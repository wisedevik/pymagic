from typing import Optional
from logic.avatar.logic_avatar_change_listener import LogicAvatarChangeListener
from logic.data.core.logic_data import LogicData
from logic.data.core.logic_data_slot import LogicDataSlot
from logic.data.data_objects.logic_mission_data import LogicMissionData
from logic.data.data_objects.logic_resource_data import LogicResourceData
from logic.home import LogicBase
from titan.debug.debugger import Debugger
from titan.util.logic_array_list import LogicArrayList


class LogicAvatar(LogicBase):
    def __init__(self) -> None:
        super().__init__()
        self.level = 0

    def init_base(self):
        self.listener = LogicAvatarChangeListener()
        self.resource_count: LogicArrayList[Optional[LogicDataSlot]] = LogicArrayList[
            Optional[LogicDataSlot]
        ]()
        self.mission_completed: LogicArrayList[Optional[LogicData]] = LogicArrayList[
            Optional[LogicData]
        ]()
        # TODO: Add all arrays

    def set_level(self, lvl: int):
        self.level = lvl

    def get_change_listener(self) -> LogicAvatarChangeListener:
        return self.listener

    def clear_data_slot_array(self, array: LogicArrayList[Optional[LogicDataSlot]]):
        if array.count >= 1:
            for i in range(array.count):
                array[i] = None

    def get_resource_count(self, resource_data: LogicResourceData):
        if resource_data.is_premium_currency() == False:
            idx = -1

            for i in range(self.resource_count.count):
                if (
                    self.resource_count[i].data.get_global_id()
                    == resource_data.get_global_id()
                ):
                    idx = i
                    break

            if idx != -1:
                return self.resource_count[i].count
        else:
            Debugger.warning(
                "LogicAvatar.get_resource_count shouldn't be used for diamonds"
            )

        return 0

    def set_resource_count(self, resource_data: LogicResourceData, cnt: int):
        if resource_data.is_premium_currency():
            Debugger.warning(
                "LogicAvatar.set_resource_count shouldn't be used for diamonds"
            )

        idx = -1

        for i in range(self.resource_count.count):
            resource = self.resource_count[i]

            if resource.data.get_global_id() == resource_data.get_global_id():
                idx = i
                break

        if idx != -1:
            self.resource_count[idx].set_count(cnt)
        else:
            Debugger.print(
                f"Added resource {resource_data.get_name()} ({resource_data.get_global_id()})"
            )
            self.resource_count.add(LogicDataSlot(resource_data, cnt))

    def set_mission_completed(self, data: LogicMissionData, state: bool):
        idx = -1

        for i in range(self.mission_completed.count):
            if self.mission_completed[i].get_global_id() == data.get_global_id():
                idx = i
                break

        if state:
            if idx == -1:
                self.mission_completed.add(data)
        else:
            if idx != -1:
                self.mission_completed.remove(idx)

    def is_client_avatar(self):
        return False

    def is_npc_avatar(self):
        return False
