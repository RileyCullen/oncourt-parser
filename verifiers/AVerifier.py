from abc import ABC, abstractmethod
from verifiers.VerificationStatus import Status

class AVerifier(ABC):
    @abstractmethod
    def verify(self, tokens: tuple) ->  Status:
        pass