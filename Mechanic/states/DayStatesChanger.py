from abc import abstractmethod
from datetime import datetime

from Mechanic.Mood import Mood
from Mechanic.states.STATE_NAMES import STATES


class TimeEdgeAndChangeAbility:
    def __init__(self, time_str, change_ability: bool):
        self.time: datetime = datetime.strptime(time_str, "%H:%M")
        self.is_able_to_change_mood = change_ability


class DayStatesChanger:

    @abstractmethod
    def get_state_by_correct_arguments(self, time: datetime, mood: Mood) -> STATES:
        pass

    def _reset(self):
        self.next_time_index = 1

    def __init__(self):
        self.next_time_index = 1
        self.last_updated_mood = Mood.NORMAL
        self.list_of_times_and_abilities = []

    def get_state(self, time, mood: Mood):
        # if self.next_time_index > len(self.list_of_times_and_abilities) - 1:
        #     self._reset()
        if time == datetime.strptime("00:00", "%H:%M"):
            self._reset()

        if self.next_time_index < len(self.list_of_times_and_abilities):
            if time >= self.list_of_times_and_abilities[self.next_time_index].time:
                self.next_time_index += 1

        current_time_box = self.list_of_times_and_abilities[self.next_time_index - 1]

        if current_time_box.is_able_to_change_mood:
            self.last_updated_mood = mood

        return self.get_state_by_correct_arguments(current_time_box.time,
                                                   self.last_updated_mood), current_time_box.is_able_to_change_mood
