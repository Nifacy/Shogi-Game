from tortoise import Model, fields, Tortoise
from tortoise.exceptions import NoValuesFetched

from services.private_room_service.domain import adapters, models


class PrivateRoomDBModel(Model):
    id = fields.IntField(pk=True)
    connection_key = fields.CharField(max_length=50, unique=True)
    connected_players: fields.ReverseRelation['PlayerDBModel']


class PlayerDBModel(Model):
    name = fields.TextField()
    connected_room: fields.ForeignKeyRelation[PrivateRoomDBModel] = fields.ForeignKeyField(
        'models.PrivateRoomDBModel', related_name='connected_players'
    )


class DefaultStorage(adapters.PrivateRoomStorage):
    async def connect(self, credentials: str):
        await Tortoise.init(
            db_url=credentials,
            modules={'models': ['services.private_room_service.infrastructure.storage']}
        )

        await Tortoise.generate_schemas()

    async def create_room(self, connection_key: models.ConnectionKey) -> models.PrivateRoom:
        record = await PrivateRoomDBModel.filter(connection_key=connection_key).first()

        if record is not None:
            raise adapters.AlreadyExists(connection_key=connection_key)

        created_record = await PrivateRoomDBModel.create(connection_key=connection_key)
        return models.PrivateRoom(_connection_key=created_record.connection_key, _players=[])

    async def remove_room(self, connection_key: models.ConnectionKey):
        record = await PrivateRoomDBModel.filter(connection_key=connection_key).first()

        if record is None:
            raise adapters.NotExists(connection_key=connection_key)

        await record.delete()

    async def update_room(self, updated_data: models.PrivateRoom) -> models.PrivateRoom:
        record = await PrivateRoomDBModel.filter(connection_key=updated_data.connection_key).first()

        if record is None:
            raise adapters.NotExists(connection_key=updated_data.connection_key)

        record.connection_key = updated_data.connection_key

        for connected_player in updated_data.players:
            player = await PlayerDBModel.filter(name=connected_player.name).first()

            if player is None:
                player = await PlayerDBModel.create(name=connected_player.name, connected_room=record)

            player.connected_room = record
            await player.save()

        await record.save()

        try:
            connected_players = await record.connected_players.all()
        except NoValuesFetched:
            connected_players = []

        return models.PrivateRoom(
            _connection_key=record.connection_key,
            _players=[models.Player(name=player.name) for player in connected_players]
        )

    async def get_room(self, connection_key: models.ConnectionKey) -> models.PrivateRoom:
        record = await PrivateRoomDBModel.filter(connection_key=connection_key).first()

        if record is None:
            raise adapters.NotExists(connection_key=connection_key)

        try:
            connected_players = await record.connected_players.all()
        except NoValuesFetched:
            connected_players = []

        return models.PrivateRoom(
            _connection_key=record.connection_key,
            _players=[models.Player(name=player.name) for player in connected_players]
        )
