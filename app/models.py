from ddd_domain_events import DomainEvents
from tortoise import Model, fields
from passlib.hash import bcrypt
from tortoise.exceptions import DoesNotExist

from app.events import RoomEvents
from app.state_builder import build_state
from app.state_converter import encode_state, decode_state


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)
    rating = fields.IntField(default=0)
    connected_room: fields.ForeignKeyNullableRelation["Room"] = fields.ForeignKeyField(
        model_name="models.Room", related_name="connected_players", null=True)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    class PydanticMeta:
        exclude = ('password_hash',)

    class Meta:
        table = "user"

    async def save(self, *args, **kwargs):
        room: Room = self.connected_room
        await super().save(*args, **kwargs)

        if room:
            DomainEvents.raise_event(
                RoomEvents.PLAYER_CONNECTED,
                room_id=room.id,
                player=self
            )

            connected_players = await room.connected_players.all()

            print("CONNECTED PLAYERS:", connected_players)
            if len(connected_players) == 2:
                player_ids = [player.id for player in connected_players]
                room.state = build_state(*player_ids)
                await room.save()

                print("RAISING EVENT....")
                DomainEvents.raise_event(
                    RoomEvents.GAME_STARTED,
                    room_id=room.id
                )


class Room(Model):
    id = fields.IntField(pk=True)
    unused = fields.BooleanField(default=False)
    state = fields.JSONField(encoder=encode_state, decoder=decode_state, null=True)

    connected_players: fields.ReverseRelation["User"]

    async def save(self, *args, **kwargs):
        try:
            in_db = await Room.get(id=self.id)
        except DoesNotExist:
            in_db = None

        if in_db and self.state != in_db.state:
            DomainEvents.raise_event(
                RoomEvents.STATE_CHANGED,
                room_id=self.id,
                state=self.state
            )

        await super().save(*args, **kwargs)

    class Meta:
        table = "room"


class PrivateRoom(Model):
    id = fields.IntField(pk=True)
    room = fields.OneToOneField(model_name="models.Room", related_name="private_room")
    connection_key = fields.CharField(50, unique=True)

    class Meta:
        table = "private_room"
