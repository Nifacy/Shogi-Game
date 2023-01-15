from game_model.game.model.id_generator import IdGenerator


class Player:
    _id_generator: IdGenerator = IdGenerator()
    _id: int

    def __init__(self, id: int = None):
        self._id = id if id is not None else self._id_generator.generate_id()

    @staticmethod
    def equals(first: "Player", second: "Player") -> bool:
        return first._id == second._id

    def __eq__(self, other: "Player") -> bool:
        return Player.equals(self, other)

    @property
    def id(self) -> int:
        return self._id

    def __repr__(self):
        return f'Player(id={self._id})'
