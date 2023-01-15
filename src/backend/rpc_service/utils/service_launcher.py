import asyncio
from rpc_service.service import BaseRpcService


class ServiceLauncher:
    """
    Объект, ответственный за защищенный запуск сервиса. Если возникнет какая-либо ошибка,
    то соединение с сервером будет обязательно закрыто.
    """

    _service: BaseRpcService

    def __init__(self, service: BaseRpcService):
        self._service = service

    async def start(self, credentials: str):
        """
        Запуск сервиса. После вызова поток исполнения блокируется. Выключить сервис
        можно комбинацией (Ctrl + C)

        :param credentials: данные для входа
        """

        try:
            print('[Service] Starting...')
            await self._service.connect(credentials)
            print('[Service] Started. For closing service type (Ctrl + C)')
            await asyncio.Future()

        # В случае, если пользователь сам захотел прекратить исполнение
        except (InterruptedError, KeyboardInterrupt):
            print('[Service] Closing...')
            await self._service.close()

        # В случае, если была внутренняя ошибка
        except Exception as e:
            await self._service.close()
            raise e
