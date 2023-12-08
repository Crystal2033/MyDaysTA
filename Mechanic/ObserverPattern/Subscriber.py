from abc import ABC, abstractmethod


class Subscriber(ABC):
    @abstractmethod
    def updateByNotify(self):
        pass
