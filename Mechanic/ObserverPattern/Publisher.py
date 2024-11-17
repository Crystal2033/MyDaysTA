from abc import ABC


class Publisher(ABC):
    def __init__(self):
        self.__observers = set()

    def attach(self, observer):
        self.__observers.add(observer)

    def detach(self, observer):
        self.__observers.remove(observer)

    def notify(self):
        for observer in self.__observers:
            observer.update_by_notify()

    def clear_all_observers(self):
        self.__observers.clear()
