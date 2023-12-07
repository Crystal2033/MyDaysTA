from Mechanic.ModelMechanic import ModelMechanic

if __name__ == "__main__":
    mech = ModelMechanic()
    mech.start()
    while True:
        end_state = input()
        split_res = end_state.split(" ")
        if split_res[0].lower() == "u":
            mech.make_mood_better(int(split_res[1]))
        elif split_res[0].lower() == "d":
            mech.make_mood_worse(int(split_res[1]))
        else:
            mech.stop()
            break
