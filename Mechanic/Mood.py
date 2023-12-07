from enum import Enum

from Mechanic.ObserverPattern.Publisher import Publisher


class Mood(Enum):
    GOOD = 0,
    NORMAL = 1,
    BAD = 2


class MoodChanger(Publisher):
    def __init__(self):
        super().__init__()
        self._moodBattery = 0
        self._MOOD_MAX_VALUE = 100
        self._MOOD_MIN_VALUE = 0

    def decrease_mood(self, delta: int = 1):
        self._moodBattery = (
            self._MOOD_MIN_VALUE if self._moodBattery - 1 < self._MOOD_MIN_VALUE else self._moodBattery - delta)
        self.notify()

    def increase_mood(self, delta: int = 1):
        self._moodBattery = (
            self._MOOD_MAX_VALUE if self._moodBattery + 1 > self._MOOD_MAX_VALUE else self._moodBattery + delta)
        self.notify()

    def get_mood(self):
        if self._moodBattery > 75:
            return Mood.GOOD
        if self._moodBattery > 40:
            return Mood.NORMAL
        return Mood.BAD
