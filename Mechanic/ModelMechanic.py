import threading
import time

from Mechanic.Mood import MoodChanger
from Mechanic.ObserverPattern.Publisher import Publisher
from Mechanic.ObserverPattern.Subscriber import Subscriber
from Mechanic.WeekTimer import WeekTimer, TimerSpeedStates, DaysPerWeek
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
    def updateByNotify(self):
        print("-----------------------------------------------")
        self._states[self._weekTimerVar.get_current_day()].get_state(
            self._weekTimerVar.get_current_time(),
            self._moodChangerVar.get_mood()
        )
        print("-----------------------------------------------")

        self.notify()  # for future UI

    def __init__(self):
        super().__init__()
        self._weekTimerVar = WeekTimer(TimerSpeedStates.FAST)
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

        self._weekTimerVar.attach(self)
        self._moodChangerVar.attach(self)

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

    def get_current_time_and_date(self):
        return self._weekTimerVar.get_current_time() + " " + self._weekTimerVar.get_current_day().name

    def start(self):
        self._weekTimerVar.start()

    def stop(self):
        self.clear_all_observers()
        self._weekTimerVar.stop()
