import json

from tortoise import Model, fields, Tortoise
from services.session_service.domain.adapters import SessionStorage, NotExists
from services.session_service.domain.factories import state_factory
from services.session_service.domain.models import SessionModel, PlayerConnectionState, PlayerModel
from settings import settings
from state_encoder import StateEncoder


class SessionDBModel(Model):
    id = fields.IntField(pk=True)
    connected_players: fields.ReverseRelation['SessionPlayerDBModel']
    state = fields.JSONField(
        encoder=lambda x: json.dumps(StateEncoder.encode(x)),
        decoder=lambda x: StateEncoder.decode(json.loads(x))
    )


class SessionPlayerDBModel(Model):
    name = fields.TextField()
    connection_state = fields.CharEnumField(PlayerConnectionState, default=PlayerConnectionState.DISCONNECTED)
    connected_session: fields.ForeignKeyRelation[SessionDBModel] = fields.ForeignKeyField(
        'models.SessionDBModel', related_name='connected_players'
    )


class SessionDatabase(SessionStorage):
    async def connect(self):
        await Tortoise.init(
            db_url=settings.postgres_dsn,
            modules={'models': ['services.session_service.infrastructure.session_database']}
        )

        await Tortoise.generate_schemas()

    async def _serialize_session(self, record: SessionDBModel) -> SessionModel:
        player_records = await record.connected_players.all()
        first_player, second_player = [PlayerModel(_name=player.name) for player in player_records]

        return SessionModel(
            _session_id=record.id,
            _players=(first_player, second_player),
            _player_connections={
                first_player.name: player_records[0].connection_state,
                second_player.name: player_records[1].connection_state
            },
            _state=record.state
        )

    async def create(self, first_player_name: str, second_player_name: str) -> SessionModel:
        first_player, second_player = PlayerModel(first_player_name), PlayerModel(second_player_name)
        state = state_factory(first_player=first_player, second_player=second_player)

        session_record = await SessionDBModel.create(state=state)
        await SessionPlayerDBModel.create(name=first_player.name, connected_session=session_record)
        await SessionPlayerDBModel.create(name=second_player_name, connected_session=session_record)

        return await self._serialize_session(session_record)

    async def get(self, session_id: int) -> SessionModel:
        record = await SessionDBModel.filter(id=session_id).first()

        if record is None:
            raise NotExists(session_id=session_id)

        return await self._serialize_session(record)

    async def update(self, updated_data: SessionModel) -> SessionModel:
        record = await SessionDBModel.filter(id=updated_data.id).first()

        if record is None:
            raise NotExists(session_id=updated_data.id)

        players = await record.connected_players.all()
        record.state = updated_data.state
        players[0].connection_state = updated_data._player_connections[players[0].name]
        players[1].connection_state = updated_data._player_connections[players[1].name]

        await players[0].save()
        await players[1].save()
        await record.save()

        return updated_data

    async def remove(self, session_id: int):
        record = await SessionDBModel.filter(id=session_id).first()

        if record is None:
            raise NotExists(session_id=session_id)

        for player in record.connected_players:
            await player.delete()

        await record.delete()
