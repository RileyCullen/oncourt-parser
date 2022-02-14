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
    gameData.append("End")
    MatchScoreL = 0
    MatchScoreR = 0
    SetScore = "0-0"
    check = True
    
    curr_set = 0
    helper = 0
    prev_entry = -1
    prev_token = ""

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
                matchData.loc[prev_entry] = ["EndSet", prev_token, str(MatchScoreL) + "-" + str(MatchScoreR)]
                curr_set += 1 
                helper = 0
            elif(check and helper == curr_set):
                matchData_length = len(matchData)
                matchData.loc[matchData_length] = ["EndGame",token, str(MatchScoreL) + "-" + str(MatchScoreR)]
                check = False
                helper = 0
                prev_entry = matchData_length
                prev_token = token
            SetScore = token
    return matchData

print(parse_entry("0-0 [*0-0] [*15-0] [*15-15] [*15-30] [*15-40] [*30-40] 0-1 [0-0*] [15-0*] [15-15*] [15-30*] [15-40*] [30-40*] 0-2 [*0-0] [*15-0] [*30-0] [*30-15] [*40-15] [*40-30] [*40-40] [*A-40] 1-2 [0-0*] [15-0*] [15-15*] [15-30*] [15-40*] 1-3 [*0-0] [*15-0] [*30-0] [*40-0] 2-3 [0-0*] [0-15*] [15-15*] [15-30*] [30-30*] [40-30*] 3-3 [*0-0] [*0-15] [*0-30] [*0-40] 3-4 [0-0*] [15-0*] [15-15*] [15-30*] [15-40*] 3-5 [*0-0] [*15-0] [*15-15] [*30-15] [*40-15] [*40-30] [*40-40] [*A-40] 4-5 [0-0*] [0-15*] [15-15*] [15-30*] [15-40*] 4-6 0-0 [*0-0] [*0-15] [*0-30] [*0-40] 4-6 0-1 [0-0*] [0-15*] [0-30*] [0-40*] 4-6 0-2 [*0-0] [*0-15] [*15-15] [*30-15] [*40-15] [*40-30] 4-6 1-2 [0-0*] [0-15*] [0-30*] [15-30*] [30-30*] [40-30*] [40-40*] [A-40*] [40-40*] [A-40*] 4-6 2-2 [*0-0] [*0-15] [*15-15] [*30-15] [*30-30] [*30-40] 4-6 2-3 [0-0*] [0-15*] [0-30*] [0-40*] 4-6 2-4 [*0-0] [*0-15] [*15-15] [*30-15] [*40-15] 4-6 3-4 [0-0*] [0-15*] [15-15*] [15-30*] [30-30*] [40-30*] [40-40*] [40-A*] 4-6 3-5 [*0-0] [*0-15] [*15-15] [*30-15] [*40-15] [*40-30] [*40-40] [*A-40] 4-6 4-5 [0-0*] [15-0*] [30-0*] [40-0*] 4-6 5-5 [*0-0] [*15-0] [*30-0] [*40-0] 4-6 6-5 [0-0*] [15-0*] [30-0*] [40-0*] [40-15*] 4-6 7-5 0-0 [*0-0] [*15-0] [*30-0] [*30-15] [*30-30] [*30-40] [*40-40] [*A-40] 4-6 7-5 1-0 [0-0*] [0-15*] [15-15*] [15-30*] [30-30*] [30-40*] [40-40*] [A-40*] 4-6 7-5 2-0 [*0-0] [*15-0] [*30-0] [*40-0] [*40-15] 4-6 7-5 3-0 [0-0*] [15-0*] [15-15*] [30-15*] [30-30*] [30-40*] 4-6 7-5 3-1 [*0-0] [*15-0] [*30-0] [*40-0] [*40-15] 4-6 7-5 4-1 [0-0*] [0-15*] [0-30*] [0-40*] [15-40*] 4-6 7-5 4-2 [*0-0] [*15-0] [*15-15] [*30-15] [*40-15] [*40-30] [*40-40] [*A-40] 4-6 7-5 5-2 [0-0*] [0-15*] [15-15*] [30-15*] [40-15*] 4-6 7-5 6-2"))

