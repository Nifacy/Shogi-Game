from game_model.game.model.id_generator import IdGenerator


class Player:
    _id_generator: IdGenerator = IdGenerator()
    _id: int

    def __init__(self):
        self._id = self._id_generator.generate_id()

    @staticmethod
    def equals(first: "Player", second: "Player") -> bool:
        return first._id == second._id

    def __eq__(self, other: "Player") -> bool:
        return Player.equals(self, other)
