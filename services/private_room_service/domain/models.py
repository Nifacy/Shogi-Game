from dataclasses import dataclass
from typing import List, NewType, Tuple

ConnectionKey = NewType('ConnectionKey', str)


class PrivateRoomFull(Exception):
    """
    Исключение, вызываемое моделью приватной комнаты в момент, когда
    происходит попытка добавить игрока в уже заполненную комнату

    Arguments:
        player - игрок, которого пытались добавить
        room - заполненная комната, в которую пытались добавить
    """

    player: 'Player'
    room: 'PrivateRoom'
    __message: str = 'Enable to add player {player!r}. Private room {room!r} is full'

    def __init__(self, player: 'Player', room: 'PrivateRoom'):
        super().__init__(self.__message.format(player=player, room=room))
        self.player = player
        self.room = room


class NotConnected(Exception):
    """
    Исключение, вызываемое моделью приватной комнаты в момент, когда
    происходит попытка отключить игрока от комнаты, к которой он не
    был подключен

    Arguments:
        player - игрок, которого пытались отключить
        room - комната, к которой не подключен игрок
    """

    player: 'Player'
    room: 'PrivateRoom'
    __message: str = 'Enable to disconnect player {player!r}. Player not connected to room {room!r}'

    def __init__(self, player: 'Player', room: 'PrivateRoom'):
        super().__init__(self.__message.format(player=player, room=room))
        self.player = player
        self.room = room


@dataclass(frozen=True)
class Player:
    """
    Бизнес модель игрока, подключенного к приватной комнате

    Arguments:
        name - имя игрока
    """

    name: str


@dataclass
class PrivateRoom:
    """
    Бизнес модель приватной комнаты
    """

    _players: List[Player]
    _connection_key: ConnectionKey
    _max_players_amount: int = 2

    def add_player(self, player: Player):
        """
        Подключает игрока к приватной комнате

        :param player: игрок, которого добавляем
        :raise PrivateRoomFull: текущая приватная комната уже заполнена
        """

        if player in self._players:
            return

        if self.is_full():
            raise PrivateRoomFull(player=player, room=self)

        self._players.append(player)

    def remove_player(self, player: Player):
        """
        Отключает игрока от приватной комнаты

        :param player: игрок, которого удаляем
        :raise NotConnected: если отключаемый игрок не был до этого подключен
        """

        if player not in self._players:
            raise NotConnected(player=player, room=self)

        self._players.remove(player)

    @property
    def players(self) -> Tuple[Player]:
        """Игроки, подключенные к приватной комнате"""
        return tuple(self._players)

    @property
    def connection_key(self) -> ConnectionKey:
        """Ключ для подключения к комнате"""
        return self._connection_key

    def is_full(self) -> bool:
        """Текущая приватная комната заполнена? """
        return len(self._players) >= self._max_players_amount

    def is_empty(self) -> bool:
        """Текущая приватная комната пустая?"""
        return len(self._players) == 0
