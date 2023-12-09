import threading
import time
from enum import Enum
from itertools import cycle
from time import sleep

from Mechanic.ObserverPattern.Publisher import Publisher


class TimerSpeedStates(Enum):
    STOP = 0,
    SLOW = 1,
    NORMAL = 2,
    SEMIFAST = 3,
    FAST = 4


class DaysPerWeek(Enum):
    SUNDAY = 0,
    MONDAY = 1,
    TUESDAY = 2,
    WEDNESDAY = 3,
    THURSDAY = 4,
    FRIDAY = 5,
    SATURDAY = 6


class WeekTimer(Publisher):

    def __init__(self, timer_init_speed: TimerSpeedStates):
        super().__init__()
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

    def stop(self):
        self.change_timer_speed_state(TimerSpeedStates.STOP)
        self.clear_all_observers()

    def change_timer_speed_state(self, new_speed_state: TimerSpeedStates):
        self._timerSpeedState = new_speed_state

    def get_current_day(self):
        return self._currentDayOfWeek

    def get_current_time(self):
        return time.strftime("%H:%M", time.gmtime(self._currentHours * 3600 + self._currentMinutes * 60))

    def increase_timer(self):
        sleep_ms_by_timer_speed_states = {TimerSpeedStates.SLOW: 0.2,
                                          TimerSpeedStates.NORMAL: 0.05,
                                          TimerSpeedStates.SEMIFAST: 0.01,
                                          TimerSpeedStates.FAST: 0.005}
        while self._timerSpeedState is not TimerSpeedStates.STOP:
            sleep(sleep_ms_by_timer_speed_states[self._timerSpeedState])
            self._currentMinutes = next(self._possibleMinutes)
            if self._currentMinutes == 0:
                self._currentHours = next(self._possibleHours)
                if self._currentHours == 0:
                    self._currentDayOfWeek = next(self._possibleDaysOfWeek)

            self.notify()
            # print(f'{self.get_current_time()} at {self._currentDayOfWeek.name}')
