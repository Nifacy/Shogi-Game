from copy import deepcopy
from typing import List

from game_model.game.manager.command import Command
from game_model.game.manager.rules import Rule, GameStateChanges
from game_model.game.model import GameState


class GameManager:
    _rules: List[Rule]
    _state: GameState

    def __init__(self, start_state: GameState):
        self._state = start_state
        self._rules = []

    def add_rule(self, rule: Rule):
        if rule not in self._rules:
            self._rules.append(rule)

    def remove_rule(self, rule: Rule):
        if rule in self._rules:
            self._rules.remove(rule)

    @property
    def game_state(self) -> GameState:
        return self._state

    def send_command(self, command: Command):
        next_state = deepcopy(self._state)
        command.execute(next_state)

        for rule in self._rules:
            rule.execute(GameStateChanges(self._state, next_state))

        self._state = next_state
