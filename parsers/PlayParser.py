import pandas as pd

def parse_entry(entry: str) -> pd.DataFrame:
    """
    This function is responsible for parsing the play-by-play data located with
    the OnCourt dataset. 

    Parameters:
    -----------
    entry: A string containing play-by-play data.

    Returns:
    --------
    A Pandas.DataFrame containing the current score, the current set score,
    and the current match score.
    """
    column_names = ["currentScore", "currentSetScore", "currentMatchScore"]
    matchData = pd.DataFrame(columns = column_names)

    gameData = entry.split(" ")
    gameData.append("E")
    MatchScoreL = 0
    MatchScoreR = 0
    SetScore = "0-0"
    check = True
    
    curr_set = 0
    helper = 0

    def updateMatchScore():  
        nonlocal MatchScoreL
        nonlocal MatchScoreR 
        if (int(SetScore[0]) > int(SetScore[2])): 
            MatchScoreL += 1
        if (int(SetScore[0]) < int(SetScore[2])):      
            MatchScoreR += 1


    for token in gameData:
        if "*" in token:   
            matchData_length = len(matchData)
            matchData.loc[matchData_length] = [token,SetScore, str(MatchScoreL) + "-" + str(MatchScoreR)]
            check = True
        elif token == "End" :
            updateMatchScore()
            matchData_length = len(matchData)
            matchData.loc[matchData_length] = [token,SetScore, str(MatchScoreL) + "-" + str(MatchScoreR)]
            check = True
        else:
            helper += 1
            if token == "0-0":
                updateMatchScore()
                curr_set += 1 
                helper = 0
            elif(check and helper == curr_set):
                matchData_length = len(matchData)
                matchData.loc[matchData_length] = ["EndGame",token, str(MatchScoreL) + "-" + str(MatchScoreR)]
                check = False
                helper = 0
            SetScore = token
    return matchData



