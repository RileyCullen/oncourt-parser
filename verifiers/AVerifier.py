from abc import ABC, abstractmethod
from enum import Enum, auto
from VerificationStatus import Status

class AVerifier(ABC):
    @abstractmethod
    def verify(self, tokens: tuple) ->  Status:
        pass