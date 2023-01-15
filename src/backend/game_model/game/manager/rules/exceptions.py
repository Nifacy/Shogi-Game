from game_model.game.manager.exceptions import ExecuteCommandException
from game_model.game.model import Player


class RulesViolation(ExecuteCommandException):
    __msg_template: str = "Нарушение правил. {violation_description}"

    def __init__(self, player: Player, description: str):
        super().__init__(player, self.__msg_template.format(violation_description=description))
