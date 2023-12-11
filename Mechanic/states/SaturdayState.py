from datetime import datetime

from Mechanic.Mood import Mood
from Mechanic.states.DayStatesChanger import DayStatesChanger, TimeEdgeAndChangeAbility
from Mechanic.states.STATE_NAMES import STATES


class SaturdayState(DayStatesChanger):
    def __init__(self):
        super().__init__()
        self.list_of_times_and_abilities = [
            TimeEdgeAndChangeAbility("00:00", True),
            TimeEdgeAndChangeAbility("11:00", True),
            TimeEdgeAndChangeAbility("11:40", True),
            TimeEdgeAndChangeAbility("12:15", False),
            TimeEdgeAndChangeAbility("15:00", True),
            TimeEdgeAndChangeAbility("15:40", True),
            TimeEdgeAndChangeAbility("20:00", True),
            TimeEdgeAndChangeAbility("20:40", True),
            TimeEdgeAndChangeAbility("22:00", True),
        ]

    def get_state_by_correct_arguments(self, time: datetime, mood: Mood) -> STATES:
        state = None
        if time == self.list_of_times_and_abilities[0].time:  # 00:00
            state = STATES.SLEEP
        elif time == self.list_of_times_and_abilities[1].time:  # 11:00
            state = STATES.EAT
        elif time == self.list_of_times_and_abilities[2].time:  # 11:40
            state = STATES.REST
        elif time == self.list_of_times_and_abilities[3].time:  # 12:15
            if self.last_updated_mood == Mood.BAD:
                state = STATES.HOBBY
            else:
                state = STATES.PC
        elif time == self.list_of_times_and_abilities[4].time:  # 15:00
            state = STATES.EAT
        elif time == self.list_of_times_and_abilities[5].time:  # 15:40
            state = STATES.PC
        elif time == self.list_of_times_and_abilities[6].time:  # 20:00
            state = STATES.EAT
        elif time == self.list_of_times_and_abilities[7].time:  # 20:40
            state = STATES.REST
        elif time == self.list_of_times_and_abilities[8].time:  # 22:00
            state = STATES.HOBBY
        if not state:
            print("Fullness of system was interrupted")
            exit(-1)
        return state
