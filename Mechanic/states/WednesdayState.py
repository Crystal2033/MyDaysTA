from datetime import datetime

from Mechanic.Mood import Mood
from Mechanic.states.DayStatesChanger import DayStatesChanger
from Mechanic.states.STATE_NAMES import STATES


class WednesdayState(DayStatesChanger):

    def get_state_by_correct_arguments(self, time: datetime, mood: Mood) -> STATES:
        pass
