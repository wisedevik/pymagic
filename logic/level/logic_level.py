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

    def set_game_listener(self, game_listener: LogicGameListener):
        self.game_listener = game_listener

    def get_state(self):
        return self.game_mode.state
    
    def get_logic_time(self) -> LogicTime:
        return self.logic_time
    
    def set_last_seen_news(self, news):
        self.logic_time = news

    def tick(self):
        ...