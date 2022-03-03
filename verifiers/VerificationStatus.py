from enum import Enum, auto
class Status(Enum):
    """
    SUCCESS: Verifier ran without running into errors in the data.

    PointVerifier:
    INVALID_PROGRESSION: Verifier ran into an error with the point progression
                         values (i.e. score went from 0-15 to 30-15)
    
    INVALID_CHANGE:      Verifier ran into an error regarding the number of 
                         point values changing (i.e. both scores change)
    """
    SUCCESS = auto()
    INVALID_PROGRESSION = auto()
    INVALID_CHANGE = auto()