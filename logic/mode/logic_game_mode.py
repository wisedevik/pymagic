from logic.command.logic_command_manager import LogicCommandManager

class LogicGameMode:

    def __init__(self):
        self.state = 1

        from logic.level.logic_level import LogicLevel
        self.level = LogicLevel(self)
        self.battle_over = False

        self.command_manager = LogicCommandManager(self.level)

    def get_state(self):
        return self.state
    
    def get_command_manager(self) -> LogicCommandManager:
        return self.command_manager
    
    def get_level(self):
        return self.level
    
    def update_one_sub_tick(self):
        logic_time = self.level.get_logic_time()

        if self.state != 2 or self.battle_over == False:
            self.command_manager.sub_tick()

            if logic_time.is_full_tick():
                self.level.tick()