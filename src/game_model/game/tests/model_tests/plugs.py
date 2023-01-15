from game_model.game.model import Figure, Position


class FigurePlug(Figure):
    def can_move(self, direction: Position) -> bool:
        return True
