from Mechanic.Mood import Mood
from Mechanic.states.DayStatesChanger import DayStatesChanger


class FridayState(DayStatesChanger):
    def get_state(self, time, mood: Mood):
        print(f"Friday {time} with {mood}")
