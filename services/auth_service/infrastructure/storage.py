from passlib.context import CryptContext
from tortoise import Model, fields, Tortoise

from services.auth_service.domain.adapters import CredentialsStorage, AlreadyRegistered, NotExists
from services.auth_service.domain.models import Password, Login
from settings import settings
from ..domain import models


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _hash_password(password: Password) -> Password:
    """
    Зашифровывает пароль, используя хеширование
    :param password: изначальный вид пароля
    :return: зашифрованный пароль
    """

    return pwd_context.hash(password)


def _verify_password(plain_password: Password, hashed_password: Password) -> bool:
    """
    Проверяет верность указанного пароля на основе зашифрованной версии исходного

    :param plain_password: пароль, который проверяем
    :param hashed_password: зашифрованная версия исходного
    :return: возвращает `True` в случае, если пароль верный, `False` - в противном
    """

    print(f'>>> {type(plain_password)}, {type(hashed_password)}')
    return pwd_context.verify(plain_password, hashed_password)


class CredentialsDBModel(Model):
    id = fields.IntField(pk=True)
    login = fields.CharField(max_length=50, unique=True)
    hashed_password = fields.CharField(max_length=200)


class CredentialsDatabase(CredentialsStorage):
    async def connect(self):
        await Tortoise.init(
            db_url=settings.postgres_dsn,
            modules={'models': ['services.auth_service.infrastructure.storage']}
        )

        await Tortoise.generate_schemas()

    async def create_record(self, credentials: models.CredentialsModel) -> models.CredentialsModel:
        record = await CredentialsDBModel.filter(login=credentials.login).first()

        if record is not None:
            raise AlreadyRegistered(credentials=credentials)

        created_record = await CredentialsDBModel.create(
            login=credentials.login,
            hashed_password=_hash_password(credentials.password))

        return models.CredentialsModel(login=created_record.login, password=created_record.hashed_password)

    async def remove_record(self, login: Login):
        record = await CredentialsDBModel.filter(login=login).first()

        if record is None:
            raise NotExists(login)

        await record.delete()

    async def get_record(self, login: str) -> models.CredentialsModel:
        record = await CredentialsDBModel.filter(login=login).first()

        if record is None:
            raise NotExists(login)

        return models.CredentialsModel(login=record.login, password=record.hashed_password)

    async def validate(self, credentials: models.CredentialsModel):
        compare_credentials = await self.get_record(credentials.login)

        if not _verify_password(credentials.password, str(compare_credentials.password)):
            raise NotExists(login=credentials.login)
