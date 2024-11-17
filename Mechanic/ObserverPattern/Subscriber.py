from abc import ABC, abstractmethod


class Subscriber(ABC):
    @abstractmethod
    def update_by_notify(self):
        pass
