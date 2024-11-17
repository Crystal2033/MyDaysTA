import threading
import time
from datetime import datetime

from Mechanic.Mood import MoodChanger, Mood
from Mechanic.ObserverPattern.Publisher import Publisher
from Mechanic.ObserverPattern.Subscriber import Subscriber
from Mechanic.WeekTimer import WeekTimer, TimerSpeedStates, DaysPerWeek
from Mechanic.states.DayStatesChanger import DayStatesChanger
from Mechanic.states.FridayState import FridayState
from Mechanic.states.MondayState import MondayState
from Mechanic.states.SaturdayState import SaturdayState
from Mechanic.states.SundayState import SundayState
from Mechanic.states.ThursdayState import ThursdayState
from Mechanic.states.TuesdayState import TuesdayState
from Mechanic.states.WednesdayState import WednesdayState


# week timer notify -> mech notify -> UI
# mood changes notify -> mech notify -> UI
class ModelMechanic(Subscriber, Publisher):
    def update_by_notify(self):
        self.current_state_automat = self._states[self._weekTimerVar.get_current_day()]
        self._time_speed = self._weekTimerVar.get_timer_speed()

        print(self._weekTimerVar.get_current_time())
        self.notify()  # for UI

    def __init__(self):
        super().__init__()
        self._time_speed = TimerSpeedStates.NORMAL
        self._weekTimerVar = WeekTimer(self._time_speed)
        self._moodChangerVar = MoodChanger()
        self._states = {
            DaysPerWeek.SUNDAY: SundayState(),
            DaysPerWeek.MONDAY: MondayState(),
            DaysPerWeek.TUESDAY: TuesdayState(),
            DaysPerWeek.WEDNESDAY: WednesdayState(),
            DaysPerWeek.THURSDAY: ThursdayState(),
            DaysPerWeek.FRIDAY: FridayState(),
            DaysPerWeek.SATURDAY: SaturdayState(),
        }
        self.current_state_automat: DayStatesChanger = self._states[self._weekTimerVar.get_current_day()]

        self._weekTimerVar.attach(self)
        self._moodChangerVar.attach(self)

    def get_state(self):
        return self.current_state_automat.get_state(datetime.strptime(self._weekTimerVar.get_current_time(), "%H:%M"),
                                                    self._moodChangerVar.get_mood())

    def get_next_state(self):
        return self.current_state_automat.get_next_state()

    def set_new_time_speed(self, time_speed: TimerSpeedStates):
        self._weekTimerVar.change_timer_speed_state(time_speed)

    def get_time_speed(self):
        return self._time_speed

    def make_mood_worse(self, amount_of_worse_units: int):
        thread = threading.Thread(target=self.mood_worse_thread, args=(amount_of_worse_units,))
        thread.start()

    def mood_worse_thread(self, amount_of_worse_units: int):
        for i in range(amount_of_worse_units):
            time.sleep(0.1)
            self._moodChangerVar.decrease_mood()

    def mood_better_thread(self, amount_of_worse_units: int):
        for i in range(amount_of_worse_units):
            time.sleep(0.1)
            self._moodChangerVar.increase_mood()

    def make_mood_better(self, amount_of_better_units: int):
        thread = threading.Thread(target=self.mood_better_thread, args=(amount_of_better_units,))
        thread.start()

    def set_mood_fast(self, new_mood: Mood):
        self._moodChangerVar.set_mood_simultaneously(new_mood)

    def get_mood(self):
        return self._moodChangerVar.get_mood()

    def get_current_time_and_date(self):
        return self._weekTimerVar.get_current_time() + " " + self._weekTimerVar.get_current_day().name

    def start(self):
        self._weekTimerVar.start()

    def stop(self):
        self.clear_all_observers()
        self._weekTimerVar.stop()
