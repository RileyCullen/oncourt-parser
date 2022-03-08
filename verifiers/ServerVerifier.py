from verifiers.AVerifier import AVerifier
from verifiers.VerificationStatus import Status

class ServerVerifier(AVerifier):
    def __init__(self, starting_server: int = -1):
        self._curr_server = starting_server

    def verify(self, tokens) -> Status:
        """
        The purpose of this function is to verify that the given server data is
        valid.

        Preconditions:
        --------------
        Note that _curr_server can be in an uninitialized state (e.g.
        _curr_server = -1), in which case the method call will still be executed
        but INVALID_SERVER will be returned to the user.

        Parameters:
        -----------
        tokens: Input tokens in the form of [curr_server]

        Returns:
        --------
        A Status enum indicating if the server scores are valid.
        """
        return Status.SUCCESS if self._curr_server == tokens[0]\
            else Status.INVALID_SERVER

    def set_server(self, server: int):
        """
        The purpose of this function is to set the current server to an 
        arbituary integer value.
        """
        self._curr_server = server

    def is_server_initialized(self) -> bool:
        """
        The purpose of this function is to check to see if _curr_server is 
        initialized to a correct value or not.
        """
        return self._curr_server != -1

    def change_server(self) -> None:
        """
        The purpose of this function is to change the server after one of the 
        following cases:
            1. A game has concluded 
            2. Or the tiebreaker score is even.
        Note that this function will change the server when called (regardless)
        of the aforementioned cases so it is up to the caller to manage when
        this function is called.
        """
        if (self._curr_server == 0):
            self._curr_server = 1
        else:
            self._curr_server = 0