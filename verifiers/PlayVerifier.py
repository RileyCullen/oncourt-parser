import pandas as pd
from verifiers.PointVerifier import PointVerifier
from verifiers.VerificationStatus import Status

def verify_play_by_play_data(play_df: pd.DataFrame, key: str):
    """
    The purpose of this function is to validate the output of the PlayParser.

    Parameters:
    -----------
    play_df: A DataFrame containing the play-by-play output from the PlayParser.

    Returns:
    --------
    An array of JSON objects that follow the format below:

        array_entry = {
            'location': {
                'set_no': set_no,
                'match_no': match_no
            },
            'type': error_type
        }
    """
    point_verifier = PointVerifier()
    logger = []
    point_num = 0

    for i, row in play_df.iterrows():
        if (row[0] != 'EndGame' and row[0] != 'EndSet' and row[0] != 'End'):
            # Remove the square brackets and asterisk from data. Split by '-'
            point_data = row[0].replace("[", "").replace("]", "")
            if (point_data.count("*") > 0):
                point_data = point_data.replace("*", "")
            point_tokens = point_data.split("-")

            point_status = point_verifier.verify(point_tokens)

            if (point_status != Status.SUCCESS):
                entry = {
                    'key': key,
                    'location': {
                        'point_num': [point_num - 1, point_num]
                    },
                    'type': point_status
                }
                logger.append(entry)
            
            point_num += 1
        else:
            point_verifier.reset()
            pass
    
    return logger