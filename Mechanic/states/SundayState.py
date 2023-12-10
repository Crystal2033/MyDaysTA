from datetime import datetime

from Mechanic.Mood import Mood
from Mechanic.states.DayStatesChanger import DayStatesChanger, TimeEdgeAndChangeAbility
from Mechanic.states.STATE_NAMES import STATES


class SundayState(DayStatesChanger):

    def get_state_by_correct_arguments(self, time: datetime, mood: Mood) -> STATES:
        state = None
        if time == self.list_of_times_and_abilities[0].time:  # 00:00
            state = STATES.SLEEP
        elif time == self.list_of_times_and_abilities[1].time:  # 14:30
            state = STATES.REST
        elif time == self.list_of_times_and_abilities[2].time:  # 19:00
            if mood is not Mood.GOOD:
                state = STATES.PC
            else:
                state = STATES.HOBBY
        elif time == self.list_of_times_and_abilities[3].time:  # 22:00
            state = STATES.EAT

        if not state:
            exit(-1)
        return state

    def get_state(self, time: datetime, mood: Mood):
        return super().get_state(time, mood)

    def __init__(self):
        super().__init__()
        self.list_of_times_and_abilities = [
            TimeEdgeAndChangeAbility("00:00", True),
            TimeEdgeAndChangeAbility("14:30", False),
            TimeEdgeAndChangeAbility("19:00", False),
            TimeEdgeAndChangeAbility("22:00", True),
        ]
