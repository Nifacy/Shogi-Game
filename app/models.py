from tortoise import Model, fields
from passlib.hash import bcrypt


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)
    rating = fields.IntField(default=0)
    connected_room = fields.ForeignKeyField(model_name="models.Room", related_name="connected_players", null=True)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    class PydanticMeta:
        exclude = ('password_hash',)

    class Meta:
        table = "user"


class Room(Model):
    id = fields.IntField(pk=True)
    unused = fields.BooleanField(default=False)
    connected_player: fields.ReverseRelation["User"]

    class Meta:
        table = "room"


class PrivateRoom(Model):
    id = fields.IntField(pk=True)
    room = fields.OneToOneField(model_name="models.Room", related_name="private_room")
    connection_key = fields.CharField(50, unique=True)

    class Meta:
        table = "private_room"
