from logic.mode.logic_game_listener import LogicGameListener
from logic.mode.logic_game_mode import LogicGameMode
from logic.time.logic_time import LogicTime


class LogicLevel:
    def __init__(self, game_mode: LogicGameMode) -> None:
        self.game_listener = None
        self.battle_started = False
        self.game_mode = game_mode
        self.logic_time = LogicTime()
        self.last_seen_news = 0
        self.battle_end_pending = False

    def set_game_listener(self, game_listener: LogicGameListener):
        self.game_listener = game_listener

    def get_state(self):
        return self.game_mode.state

    def get_logic_time(self) -> LogicTime:
        return self.logic_time

    def is_in_combat_state(self):
        state = self.get_state()
        return state == 2 or state == 3 or state == 5

    def set_last_seen_news(self, news):
        self.last_seen_news = news

    def get_battle_end_pending(self):
        return self.battle_end_pending

    def sub_tick(self): ...

    def tick(self): ...
