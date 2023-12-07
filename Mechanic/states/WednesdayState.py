from Mechanic.Mood import Mood
from Mechanic.states.DayStatesChanger import DayStatesChanger


class WednesdayState(DayStatesChanger):
    def get_state(self, time, mood: Mood):
        print(f"Wednesday {time} with {mood}")
