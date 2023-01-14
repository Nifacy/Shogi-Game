import asyncio
from contracts import private_room_service
from rpc_service import RpcServiceBuilder
from rpc_service.utils import ServiceLauncher
from services.private_room_service import infrastructure, event_handlers
from services.private_room_service.methods import Implementation
from settings import settings

client = infrastructure.SessionServiceClient()
db = infrastructure.DefaultStorage()
builder = infrastructure.DefaultRoomBuilder(db)

implementation = Implementation(database=db, builder=builder, client=client)
service = RpcServiceBuilder.from_contract(implementation, private_room_service.Contract)
launcher = ServiceLauncher(service=service)
loop = asyncio.get_event_loop()


async def open_connections():
    await db.connect()
    await client.connect(settings.amqp_dsn)
    event_handlers.bind_handlers()
    await event_handlers.amqp_publisher.connect(settings.amqp_dsn)
    await launcher.start(settings.amqp_dsn)


async def close_connections():
    await client.close()
    await event_handlers.amqp_publisher.close()


if __name__ == '__main__':
    try:
        asyncio.run(open_connections())
    except KeyboardInterrupt:
        asyncio.run(close_connections())
