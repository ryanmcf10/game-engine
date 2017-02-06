from abc import ABCMeta, abstractmethod

class Environment(metaclass=ABCMeta):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def handle_actions(self, actions):
        pass

    @abstractmethod
    def load_new_env(self, environment):
        pass

    @abstractmethod
    def load_metadata(self, metadata):
        pass

    @abstractmethod
    def save_metadata(self):
        pass
