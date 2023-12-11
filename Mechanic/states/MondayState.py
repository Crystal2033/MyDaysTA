from datetime import datetime

from Mechanic.Mood import Mood
from Mechanic.states.DayStatesChanger import DayStatesChanger, TimeEdgeAndChangeAbility
from Mechanic.states.STATE_NAMES import STATES


class MondayState(DayStatesChanger):

    def __init__(self):
        super().__init__()
        self.list_of_times_and_abilities = [
            TimeEdgeAndChangeAbility("00:00", True),
            TimeEdgeAndChangeAbility("06:50", True),
            TimeEdgeAndChangeAbility("07:30", True),
            TimeEdgeAndChangeAbility("09:00", True),
            TimeEdgeAndChangeAbility("14:30", True),
            TimeEdgeAndChangeAbility("16:00", True),
            TimeEdgeAndChangeAbility("16:40", True),
            TimeEdgeAndChangeAbility("18:00", False),
            TimeEdgeAndChangeAbility("21:30", True),
            TimeEdgeAndChangeAbility("22:10", True),
        ]

    def get_state_by_correct_arguments(self, time: datetime, mood: Mood) -> STATES:
        state = None
        if time == self.list_of_times_and_abilities[0].time:  # 00:00
            state = STATES.SLEEP
        elif time == self.list_of_times_and_abilities[1].time:  # 06:50
            state = STATES.EAT
        elif time == self.list_of_times_and_abilities[2].time:  # 07:30
            state = STATES.ROAD
        elif time == self.list_of_times_and_abilities[3].time:  # 09:00
            state = STATES.UNIVERSITY
        elif time == self.list_of_times_and_abilities[4].time:  # 14:30
            state = STATES.ROAD
        elif time == self.list_of_times_and_abilities[5].time:  # 16:00
            state = STATES.EAT
        elif time == self.list_of_times_and_abilities[6].time:  # 16:40
            state = STATES.REST
        elif time == self.list_of_times_and_abilities[7].time:  # 18:00
            if self.last_updated_mood == Mood.BAD:
                state = STATES.HOBBY
            else:
                state = STATES.PC
        elif time == self.list_of_times_and_abilities[8].time:  # 21:30
            state = STATES.EAT
        elif time == self.list_of_times_and_abilities[9].time:  # 22:10
            state = STATES.HOBBY
        if not state:
            print("Fullness of system was interrupted")
            exit(-1)
        return state
