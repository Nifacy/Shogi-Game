import asyncio
from contracts import searcher_service
from rpc_service import RpcServiceBuilder
from rpc_service.utils import ServiceLauncher
from services.searcher_service import infrastructure, event_handlers
from services.searcher_service.methods import Implementation
from .settings import settings

client = infrastructure.SessionServiceClient()
db = infrastructure.DefaultStorage()
implementation = Implementation(database=db, client=client)
service = RpcServiceBuilder.from_contract(implementation, searcher_service.Contract)
launcher = ServiceLauncher(service=service)


async def init_infrastructure():
    await client.connect(settings.amqp_dsn)
    await event_handlers.amqp_publisher.connect(settings.amqp_dsn)
    await launcher.start(settings.amqp_dsn)


async def close_infrastructure():
    await client.close()
    await event_handlers.amqp_publisher.close()


if __name__ == '__main__':
    try:
        asyncio.run(init_infrastructure())
    except (KeyboardInterrupt, InterruptedError):
        asyncio.run(close_infrastructure())
