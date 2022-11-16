from tortoise import Model, fields
from passlib.hash import bcrypt


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)
    rating = fields.IntField(default=0)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    class PydanticMeta:
        exclude = ('password_hash',)
