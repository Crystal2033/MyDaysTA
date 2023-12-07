from Mechanic.Mood import Mood
from Mechanic.states.DayStatesChanger import DayStatesChanger


class ThursdayState(DayStatesChanger):
    def get_state(self, time, mood: Mood):
        print(f"Thursday {time} with {mood}")
