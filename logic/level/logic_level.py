from logic.mode.logic_game_listener import LogicGameListener


class LogicLevel:
    def __init__(self) -> None:
        self.game_listener = None
        self.battle_started = False

    def set_game_listener(self, game_listener: LogicGameListener):
        self.game_listener = game_listener
