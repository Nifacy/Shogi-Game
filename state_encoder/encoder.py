from itertools import product

from game_model.figures import Lion, Elephant, Giraffe, Chicken, Hen
from game_model.game.model import Player, Figure, Prison, Board, GameState, Position, GameStatus


class PlayerConverter(Player):
    @classmethod
    def encode(cls, player: Player) -> dict:
        return {"id": player._id}

    @classmethod
    def decode(cls, player_encoded: dict) -> Player:
        return Player(id=player_encoded["id"])


class FigureConverter(Figure):
    _figures_classes = {
        "Lion": Lion,
        "Elephant": Elephant,
        "Giraffe": Giraffe,
        "Chicken": Chicken,
        "Hen": Hen
    }

    @classmethod
    def encode(cls, figure: Figure) -> dict:
        return {
            "owner": PlayerConverter.encode(figure.owner),
            "type": figure.__class__.__name__,
            "id": figure._id
        }

    @classmethod
    def decode(cls, figure_encoded: dict) -> Figure:
        owner = PlayerConverter.decode(figure_encoded["owner"])
        figure = cls._figures_classes[figure_encoded["type"]](owner=owner)
        figure._id = figure_encoded["id"]

        return figure


class PrisonConverter(Prison):
    @classmethod
    def encode(cls, prison: Prison) -> dict:
        return {
            "figures": [FigureConverter.encode(figure) for figure in prison.figures],
            "owner": PlayerConverter.encode(prison._owner)
        }

    @classmethod
    def decode(cls, prison_encoded: dict) -> Prison:
        owner = PlayerConverter.decode(prison_encoded["owner"])
        prison = Prison(owner=owner)

        for figure in prison_encoded["figures"]:
            figure = FigureConverter.decode(figure)
            prison.add_figure(figure)

        return prison


class BoardConverter(Board):
    @classmethod
    def _encode_cell(cls, position: Position, figure: Figure) -> dict:
        return {
            "position": position._asdict(),
            "figure": FigureConverter.encode(figure)
        }

    @classmethod
    def _decode_cell(cls, encoded_cell: dict) -> (Position, Figure):
        position = Position(**encoded_cell["position"])
        figure = FigureConverter.decode(encoded_cell["figure"])

        return position, figure

    @classmethod
    def encode(cls, board: Board) -> dict:
        cells = []

        for pos in product(*map(range, board.size)):
            pos = Position(*pos)
            cell = board.get_cell(pos)

            if not cell.is_empty():
                cells.append(cls._encode_cell(pos, cell.get_figure()))

        return {
            "size": list(board.size),
            "cells": cells
        }

    @classmethod
    def decode(cls, board_encoded: dict) -> Board:
        board = Board(size=tuple(board_encoded["size"]))

        for pos, figure in map(cls._decode_cell, board_encoded["cells"]):
            board.get_cell(pos).put_figure(figure)

        return board


class StateEncoder(GameState):
    @classmethod
    def encode(cls, state: GameState) -> dict:
        return {
            "status": state.status.value,
            "first_player": PlayerConverter.encode(state.first_player),
            "second_player": PlayerConverter.encode(state.second_player),
            "board": BoardConverter.encode(state.board),
            "first_player_prison": PrisonConverter.encode(state.first_player_prison),
            "second_player_prison": PrisonConverter.encode(state.second_player_prison)
        }

    @classmethod
    def decode(cls, state_encoded: dict) -> GameState:
        return GameState(
            status=GameStatus(state_encoded["status"]),
            first_player=PlayerConverter.decode(state_encoded["first_player"]),
            second_player=PlayerConverter.decode(state_encoded["second_player"]),
            board=BoardConverter.decode(state_encoded["board"]),
            first_player_prison=PrisonConverter.decode(state_encoded["first_player_prison"]),
            second_player_prison=PrisonConverter.decode(state_encoded["second_player_prison"])
        )
