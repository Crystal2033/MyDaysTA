from abc import ABC, abstractmethod

from Mechanic.Mood import Mood


class DayStatesChanger(ABC):
    @abstractmethod
    def get_state(self, time, mood: Mood):
        pass

