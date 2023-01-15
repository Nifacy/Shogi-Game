import asyncio

from contracts import account_service
from rpc_service.utils import ServiceLauncher
from services.accounts_service.infrastructure import AccountDatabase
from services.accounts_service.methods import Implementation
from rpc_service import RpcServiceBuilder
from settings import settings


db = AccountDatabase()
implementation = Implementation(storage=db)
service = RpcServiceBuilder.from_contract(implementation, account_service.Contract)
launcher = ServiceLauncher(service)


async def main():
    await db.connect()
    await launcher.start(settings.amqp_dsn)


if __name__ == '__main__':
    asyncio.run(main())
