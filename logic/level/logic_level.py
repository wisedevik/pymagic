from logic.home.logic_client_home import LogicClientHome
from logic.mode.logic_game_listener import LogicGameListener
from logic.mode.logic_game_mode import LogicGameMode
from logic.time.logic_time import LogicTime
from titan.json.logic_json_boolean import LogicJSONBoolean
from titan.json.logic_json_number import LogicJSONNumber
from titan.json.logic_json_object import LogicJSONObject


class LogicLevel:
    def __init__(self, game_mode: "LogicGameMode") -> None:
        self.game_listener = None
        self.battle_started = False
        self.game_mode = game_mode
        self.logic_time = LogicTime()
        self.last_seen_news = 0
        self.battle_end_pending = False
        self.wave_number = 0
        self.android_client = True
        self.home: LogicClientHome = LogicClientHome()

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

    def set_home(self, home):
        self.home = home

    def get_home(self):
        return self.home

    def get_battle_end_pending(self):
        return self.battle_end_pending

    def sub_tick(self): ...

    def tick(self): ...

    def save_to_json(self, json_obj: LogicJSONObject):
        if (self.wave_number >= 1):
            json_obj.put("wave_num", LogicJSONNumber(self.wave_number))

        if (self.android_client):
            json_obj.put("android_client", LogicJSONBoolean(self.android_client))

        json_obj.put("last_news_seen", LogicJSONNumber(self.last_seen_news))
