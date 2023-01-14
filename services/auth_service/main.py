import asyncio
from contracts import auth_service
from rpc_service import RpcServiceBuilder
from rpc_service.utils import ServiceLauncher
from services.auth_service import infrastructure
from services.auth_service.methods import Implementation
from settings import settings


db = infrastructure.CredentialsDatabase()
secrets = infrastructure.JWTSecrets(key='MY_WIFE_LEFT_ME', algorithm='HS256')
jwt = infrastructure.JWTMethod(db, secrets)

implementation = Implementation(database=db, validate_method=jwt)
service = RpcServiceBuilder.from_contract(implementation, auth_service.Contract)
launcher = ServiceLauncher(service)


async def main():
    await db.connect()
    await launcher.start(settings.amqp_dsn)


if __name__ == '__main__':
    asyncio.run(main())
