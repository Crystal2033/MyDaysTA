from Mechanic.Mood import Mood
from Mechanic.states.DayStatesChanger import DayStatesChanger


class SaturdayState(DayStatesChanger):
    def get_state(self, time, mood: Mood):
        print(f"Saturday {time} with {mood}")
