import asyncio
from contracts import session_service
from rpc_service import RpcServiceBuilder
from rpc_service.utils import ServiceLauncher
from services.session_service import event_handlers
from services.session_service.infrastructure.session_database import SessionDatabase
from services.session_service.methods import Implementation
from .settings import settings


db = SessionDatabase()
implementation = Implementation(database=db)

service = RpcServiceBuilder.from_contract(implementation, session_service.Contract)
launcher = ServiceLauncher(service)


async def main():
    await db.connect(settings.postgres_dsn)
    await event_handlers.amqp_publisher.connect(settings.amqp_dsn)
    await launcher.start(settings.amqp_dsn)


if __name__ == "__main__":
    print(f'<<<<<<<<<<<<<<<<<<< {id(session_service.ExecuteCommandError)}')
    asyncio.run(main())
