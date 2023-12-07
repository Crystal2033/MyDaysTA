from Mechanic.Mood import Mood
from Mechanic.states.DayStatesChanger import DayStatesChanger


class MondayState(DayStatesChanger):
    def get_state(self, time, mood: Mood):
        print(f"Monday {time} with {mood}")
