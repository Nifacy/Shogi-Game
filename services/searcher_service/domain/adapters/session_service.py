from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, NewType
from .. import models


SessionId = NewType('SessionId', int)


@dataclass(frozen=True)
class Session:
    """
    Value Object созданной сессии

    Arguments:
        id - идентификатор созданной сессии
    """

    id: SessionId


class SessionServiceAdapter(ABC):
    """
    Адаптер к сервису игровых сессий
    """

    @abstractmethod
    async def create_session(self, players: Iterable[models.WaitingPlayer]) -> Session:
        """
        Посылает запрос сервису на создание игровой сессии для игроков

        :param players: игроки, для которых создается игровая сессия
        :return: созданная сессия
        """
        raise NotImplementedError()
