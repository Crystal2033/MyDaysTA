from Mechanic.Mood import Mood
from Mechanic.states.DayStatesChanger import DayStatesChanger


class SundayState(DayStatesChanger):
    def get_state(self, time, mood: Mood):
        print(f"Sunday {time} with {mood}")