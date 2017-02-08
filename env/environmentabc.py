from abc import ABCMeta, abstractmethod

"""
ENVIRONMENT

Abstract Base Class from which all game environments derive.

Defines a common interface for each environment.

"""
class Environment(metaclass=ABCMeta):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def scale(self):
        pass
