from logic.command.logic_command_manager import LogicCommandManager
from logic.time.logic_timer import LogicTimer
from titan.debug.debugger import Debugger


class LogicGameMode:

    def __init__(self):
        self.state = 1

        from logic.level.logic_level import LogicLevel

        self.level = LogicLevel(self)
        self.battle_over = False
        self.visitor_avatar = None
        self.home_owner_avatar = None
        self.battle_timer: LogicTimer | None = None

        self.command_manager = LogicCommandManager(self.level)

    def get_visitor_avatar(self):
        return self.visitor_avatar

    def get_home_owner_avatar(self):
        return self.home_owner_avatar

    def set_visitor_avatar(self, avatar):
        self.visitor_avatar = avatar

    def set_home_owner_avatar(self, avatar):
        self.home_owner_avatar = avatar

    def get_state(self):
        return self.state

    def get_command_manager(self) -> LogicCommandManager:
        return self.command_manager

    def get_level(self):
        return self.level

    def set_battle_over(self):
        if self.battle_over:
            return

        self.battle_over = True

    def sub_tick(self):
        self.command_manager.sub_tick()
        self.level.sub_tick()

    def tick(self):
        self.level.tick()

    def update_one_sub_tick(self):
        logic_time = self.level.get_logic_time()

        if self.state != 2 or self.battle_over == False:
            self.sub_tick()

            if logic_time.is_full_tick():
                self.tick()

        if self.level.is_in_combat_state():
            if (
                self.battle_timer
                and self.battle_timer.get_remaining_seconds(logic_time) == 0
                or self.level.get_battle_end_pending()
            ):
                self.set_battle_over()

        logic_time.increase_sub_tick()
