from abc import ABC, abstractmethod
from .. import models


class PrivateRoomBuilder(ABC):
    """Интерфейс для фабрики приватных комнат"""

    @abstractmethod
    async def generate_room(self) -> models.PrivateRoom:
        """
        Генерирует пустую приватную комнату

        :return: сгенерированная комната
        """
        raise NotImplementedError()
