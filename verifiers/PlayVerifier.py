import pandas as pd
from verifiers.PointVerifier import PointVerifier
from verifiers.VerificationStatus import Status
from verifiers.ServerVerifier import ServerVerifier

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
    server_verifier = ServerVerifier()
    logger = []
    point_num = 0

    is_tie_breaker = False

    for i, row in play_df.iterrows():
        if (row[0] != 'EndGame' and row[0] != 'EndSet' and row[0] != 'End'):
            # Remove the square brackets and asterisk from data. Split by '-'
            point_data = row[0].replace("[", "").replace("]", "")

            server = -1
            server_status = Status.NO_SERVER_ENTRY
            if (point_data.count("*") > 0):
                server = 0 if point_data.index("*") == 0 else 1
                if (not server_verifier.is_server_initialized()):
                    server_verifier.set_server(server)

                server_status = server_verifier.verify([server])

                point_data = point_data.replace("*", "")
            point_tokens = point_data.split("-")

            if (is_tie_breaker and int(point_tokens[0]) + int(point_tokens[1])):
                server_verifier.change_server()

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

            if (server_status == Status.NO_SERVER_ENTRY):
                entry = {
                    'key': key, 
                    'location': {
                        'point_num': [point_num]
                    },
                    'type': Status.NO_SERVER_ENTRY
                }
                logger.append(entry)
            elif (server_status == Status.INVALID_SERVER):
                entry = {
                    'key': key, 
                    'location': {
                        'point_num': [point_num - 1, point_num]
                    },
                    'type': Status.INVALID_SERVER
                }
                logger.append(entry) 
            
            point_num += 1
        else:
            if (is_tie_breaker): is_tie_breaker = False
            if (row[1] == "6-6"): is_tie_breaker = True

            point_verifier.reset()
            server_verifier.change_server()
    
    return logger