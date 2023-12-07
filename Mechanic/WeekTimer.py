import threading
from enum import Enum
from itertools import cycle
from time import sleep


class TimerSpeedStates(Enum):
    STOP = 0,
    SLOW = 1,
    NORMAL = 2,
    FAST = 3


class DaysPerWeek(Enum):
    SUNDAY = 0,
    MONDAY = 1,
    TUESDAY = 2,
    WEDNESDAY = 3,
    THURSDAY = 4,
    FRIDAY = 5,
    SATURDAY = 6


class WeekTimer:

    def __init__(self, timer_init_speed: TimerSpeedStates):
        self._timerSpeedState = timer_init_speed
        self._possibleHours = cycle([i for i in range(24)])
        self._possibleMinutes = cycle([i for i in range(60)])
        self._possibleDaysOfWeek = cycle([DaysPerWeek.SUNDAY,
                                          DaysPerWeek.MONDAY,
                                          DaysPerWeek.TUESDAY,
                                          DaysPerWeek.WEDNESDAY,
                                          DaysPerWeek.THURSDAY,
                                          DaysPerWeek.FRIDAY,
                                          DaysPerWeek.SATURDAY])
        self._currentHours = 0
        self._currentMinutes = 0
        self._currentDayOfWeek = DaysPerWeek.SUNDAY
        self._timerThread = threading.Thread(target=self.increase_timer)

    def start(self):
        self._timerThread.start()

    def change_timer_speed_state(self, new_speed_state: TimerSpeedStates):
        self._timerSpeedState = new_speed_state

    def increase_timer(self):
        sleep_ms_by_timer_speed_states = {TimerSpeedStates.SLOW: 0.2,
                                          TimerSpeedStates.NORMAL: 0.05,
                                          TimerSpeedStates.FAST: 0.005}
        while self._timerSpeedState is not TimerSpeedStates.STOP:
            sleep(sleep_ms_by_timer_speed_states[self._timerSpeedState])
            self._currentMinutes = next(self._possibleMinutes)
            if self._currentMinutes == 0:
                self._currentHours = next(self._possibleHours)
                if self._currentHours == 0:
                    self._currentDayOfWeek = next(self._possibleDaysOfWeek)

            print(f'{self._currentHours:02d}:{self._currentMinutes:02d} at {self._currentDayOfWeek.name}')
