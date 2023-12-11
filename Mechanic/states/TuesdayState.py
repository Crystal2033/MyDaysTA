from datetime import datetime

from Mechanic.Mood import Mood
from Mechanic.states.DayStatesChanger import DayStatesChanger, TimeEdgeAndChangeAbility
from Mechanic.states.STATE_NAMES import STATES


class TuesdayState(DayStatesChanger):
    def __init__(self):
        super().__init__()
        self.list_of_times_and_abilities = [
            TimeEdgeAndChangeAbility("00:00", True),
            TimeEdgeAndChangeAbility("09:30", True),
            TimeEdgeAndChangeAbility("10:10", True),
            TimeEdgeAndChangeAbility("13:00", True),
            TimeEdgeAndChangeAbility("17:30", True),
            TimeEdgeAndChangeAbility("18:10", True),
            TimeEdgeAndChangeAbility("19:00", False),
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
        elif time == self.list_of_times_and_abilities[3].time:  # 13:00
            state = STATES.PC
        elif time == self.list_of_times_and_abilities[4].time:  # 17:30
            state = STATES.EAT
        elif time == self.list_of_times_and_abilities[5].time:  # 18:10
            state = STATES.REST
        elif time == self.list_of_times_and_abilities[6].time:  # 19:00
            if self.last_updated_mood == Mood.GOOD:
                state = STATES.PC
            else:
                state = STATES.HOBBY
        elif time == self.list_of_times_and_abilities[7].time:  # 21:30
            state = STATES.EAT
        elif time == self.list_of_times_and_abilities[8].time:  # 22:10
            state = STATES.HOBBY
        if not state:
            print("Fullness of system was interrupted")
            exit(-1)
        return state
