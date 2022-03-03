from verifiers.AVerifier import AVerifier
from verifiers.VerificationStatus import Status


class PointVerifier(AVerifier):
    def __init__(self) -> None:
        self._p1_score = "0"
        self._p2_score = "0"

        self._has_reset = False

        self._prev_p1_score = "0"
        self._prev_p2_score = "0"

    def reset(self):
        """
        The purpose of this function is to reset the PointVerifier after a match
        has concluded.
        """
        self._has_reset = True
        self._prev_p1_score = self._p1_score
        self._prev_p2_score = self._p2_score
        self._p1_score = "0"
        self._p2_score = "0"

    def verify(self, tokens) -> Status:
        """
        The purpose of this function is to verify the point scores given a set 
        of input tokens. 

        Parameters:
        -----------
        tokens: Input tokens in the form of [p1_score, p2_score].

        Returns:
        --------
        A Status enum indicating if the point values are valid.
        """
        p1_curr_score = tokens[0]
        p2_curr_score = tokens[1]

        verify_change = self._verify_one_change(p1_curr_score, p2_curr_score)
        verify_point  = self._verify_point_progression(p1_curr_score, 1) and \
            self._verify_point_progression(p2_curr_score, 2)

        self._p1_score = p1_curr_score
        self._p2_score = p2_curr_score
        self._has_reset = False

        if (not verify_change): return Status.INVALID_CHANGE
        if (not verify_point): return Status.INVALID_PROGRESSION
        return Status.SUCCESS
    
    def get_timestamp(self) -> dict:
        """
        This function returns the current set_no and game_no values. Note that 
        this function must be immediately called after verify in order to obtain
        the correct location data.

        Returns:
        --------
        A Python dictionary containing locati
        """
        return {
            'set_no': self._set_no,
            'game_no': self._game_no
        }
    
    def _verify_one_change(self, p1_score, p2_score) -> bool:
        """
        The purpose of this function is to verify that only one score has 
        changed.

        Parameters:
        -----------
        p1_score: Player one's score.
        p2_score: Player two's score.

        Returns: 
        --------
        Returns a boolean indicating if only one score has changed.
        """
        if (self._has_reset): return True
        return (p1_score == self._p1_score and p2_score != self._p2_score) or \
            (p1_score != self._p1_score and p2_score == self._p2_score)

    def _verify_point_progression(self, curr_point: str, player: int) -> bool:
        """
        This is a helper function that assists with the verification of point 
        scores. More specifically, this function is responsible for validating
        that the score progressions.

        Parameters:
        -----------
        curr_point: The current score.
        player: The player that corresonds to curr_point.

        Returns:
        --------
        Returns a boolean denoting whether both the score progression is valid.
        """

        prev_point = self._p1_score if player == 1 else self._p2_score

        if prev_point == '0': return (curr_point == '0' or curr_point == '15' or curr_point == '1')
        elif prev_point == '15': return (curr_point == '15' or curr_point == '30')
        elif prev_point == '30': return (curr_point == '30' or curr_point == '40')
        elif prev_point == '40': return (curr_point == '40' or curr_point == 'A')
        elif prev_point == 'A': return (curr_point == '40') 
        else: return (curr_point == prev_point or int(curr_point) == int(prev_point) + 1)