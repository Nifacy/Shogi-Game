from tortoise import Model, fields, Tortoise
from services.accounts_service.domain import adapters, AccountModel


class AccountDBModel(Model):
    """Tortoise модель представления данных об аккаунте пользователя"""

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    rating = fields.IntField(default=0)


class AccountDatabase:
    """Реализация хранилища аккаунтов на основе Postgres и Tortoise ORM"""

    async def connect(self, credentials):
        await Tortoise.init(
            db_url=credentials,
            modules={'models': ['services.accounts_service.infrastructure.account_database']}
        )

        await Tortoise.generate_schemas()

    async def create(self, username: str) -> AccountModel:
        is_exists = await AccountDBModel.filter(username=username).exists()

        if is_exists:
            raise adapters.AlreadyExists(username=username)

        created_record = await AccountDBModel.create(username=username)
        return AccountModel(username=created_record.username, rating=created_record.rating)

    async def get(self, username: str) -> AccountModel:
        record = await AccountDBModel.filter(username=username).first()

        if record is None:
            raise adapters.NotExists(username=username)

        return AccountModel(username=record.username, rating=record.rating)

    async def update(self, updated_data: AccountModel) -> AccountModel:
        record = await AccountDBModel.filter(username=updated_data.username).first()

        if record is None:
            raise adapters.NotExists(username=updated_data.username)

        record.username = updated_data.username
        record.rating = updated_data.rating
        await record.save()

        return await self.get(updated_data.username)

    async def remove(self, username: str):
        record = await AccountDBModel.filter(username=username).first()

        if record is None:
            raise adapters.NotExists(username=username)

        await record.delete()
