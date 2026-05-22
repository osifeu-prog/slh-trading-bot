from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    @abstractmethod
    def on_bar(self, bar):
        pass

    @abstractmethod
    def get_signal(self):
        pass
