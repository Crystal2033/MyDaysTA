from datetime import datetime

from Mechanic.Mood import Mood
from Mechanic.states.DayStatesChanger import DayStatesChanger, TimeEdgeAndChangeAbility
from Mechanic.states.STATE_NAMES import STATES


class SundayState(DayStatesChanger):

    def get_state_by_correct_arguments(self, time: datetime, mood: Mood) -> STATES:
        state = None
        if time == self.list_of_times_and_abilities[0].time:  # 00:00
            state = STATES.SLEEP
        elif time == self.list_of_times_and_abilities[1].time:  # 10:00
            state = STATES.EAT
        elif time == self.list_of_times_and_abilities[2].time:  # 10:25
            state = STATES.PC
        elif time == self.list_of_times_and_abilities[3].time:  # 14:00
            state = STATES.EAT
        elif time == self.list_of_times_and_abilities[4].time:  # 14:30
            state = STATES.REST
        elif time == self.list_of_times_and_abilities[5].time:  # 15:30
            state = STATES.PC
        elif time == self.list_of_times_and_abilities[6].time:  # 21:30
            state = STATES.EAT
        elif time == self.list_of_times_and_abilities[7].time:  # 22:00
            state = STATES.HOBBY
        if not state:
            exit(-1)
        return state

    def get_state(self, time: datetime, mood: Mood):
        return super().get_state(time, mood)

    def __init__(self):
        super().__init__()
        self.list_of_times_and_abilities = [
            TimeEdgeAndChangeAbility("00:00", True),
            TimeEdgeAndChangeAbility("10:00", True),
            TimeEdgeAndChangeAbility("10:40", True),
            TimeEdgeAndChangeAbility("14:00", True),
            TimeEdgeAndChangeAbility("14:40", True),
            TimeEdgeAndChangeAbility("15:40", True),
            TimeEdgeAndChangeAbility("21:30", True),
            TimeEdgeAndChangeAbility("22:10", True),
        ]
