from Mechanic.Mood import Mood
from Mechanic.states.DayStatesChanger import DayStatesChanger


class TuesdayState(DayStatesChanger):
    def get_state(self, time, mood: Mood):
        print(f"Tuesday {time} with {mood}")
