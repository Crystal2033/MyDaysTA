from Mechanic.WeekTimer import WeekTimer, TimerSpeedStates

if __name__ == "__main__":
    timer = WeekTimer(timer_init_speed=TimerSpeedStates.NORMAL)
    timer.start()
    while True:
        end_state = input()
        if end_state.lower() == "n":
            timer.change_timer_speed_state(TimerSpeedStates.NORMAL)
        elif end_state.lower() == "f":
            timer.change_timer_speed_state(TimerSpeedStates.FAST)
        elif end_state.lower() == "s":
            timer.change_timer_speed_state(TimerSpeedStates.SLOW)
        elif end_state.lower() == "e":
            timer.change_timer_speed_state(TimerSpeedStates.STOP)
            break
