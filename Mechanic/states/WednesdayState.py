from datetime import datetime

from Mechanic.Mood import Mood
from Mechanic.states.DayStatesChanger import DayStatesChanger, TimeEdgeAndChangeAbility
from Mechanic.states.STATE_NAMES import STATES


class WednesdayState(DayStatesChanger):
    def __init__(self):
        super().__init__()
        self.list_of_times_and_abilities = [
            TimeEdgeAndChangeAbility("00:00", True),
            TimeEdgeAndChangeAbility("09:30", True),
            TimeEdgeAndChangeAbility("10:10", True),
            TimeEdgeAndChangeAbility("10:55", True),
            TimeEdgeAndChangeAbility("14:30", True),
            TimeEdgeAndChangeAbility("15:10", False),
            TimeEdgeAndChangeAbility("16:30", True),
            TimeEdgeAndChangeAbility("21:30", True),
            TimeEdgeAndChangeAbility("22:10", True),
        ]

    def get_state_by_correct_arguments(self, time: datetime, mood: Mood) -> STATES:
        state = None
        if time == self.list_of_times_and_abilities[0].time:  # 00:00
            state = STATES.SLEEP
        elif time == self.list_of_times_and_abilities[1].time:  # 09:30
            state = STATES.EAT
        elif time == self.list_of_times_and_abilities[2].time:  # 10:10
            state = STATES.REST
        elif time == self.list_of_times_and_abilities[3].time:  # 10:55
            state = STATES.PC
        elif time == self.list_of_times_and_abilities[4].time:  # 14:30
            state = STATES.EAT
        elif time == self.list_of_times_and_abilities[5].time:  # 15:10
            if self.last_updated_mood == Mood.BAD:
                state = STATES.WALK
            else:
                state = STATES.REST
        elif time == self.list_of_times_and_abilities[6].time:  # 16:30
            state = STATES.PC
        elif time == self.list_of_times_and_abilities[7].time:  # 21:30
            state = STATES.EAT
        elif time == self.list_of_times_and_abilities[8].time:  # 22:10
            state = STATES.HOBBY
        if not state:
            print("Fullness of system was interrupted")
            exit(-1)
        return state
