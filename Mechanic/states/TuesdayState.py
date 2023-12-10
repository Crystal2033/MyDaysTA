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
            TimeEdgeAndChangeAbility("12:35", True),
            TimeEdgeAndChangeAbility("13:15", True),
            TimeEdgeAndChangeAbility("18:00", False),
            TimeEdgeAndChangeAbility("19:00", False),
            TimeEdgeAndChangeAbility("21:30", True),
            TimeEdgeAndChangeAbility("22:10", True),
        ]

    def get_state_by_correct_arguments(self, time: datetime, mood: Mood) -> STATES:
        pass
