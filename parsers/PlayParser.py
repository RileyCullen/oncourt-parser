import pandas as pd



def parse_entry(entry):
   
    column_names = ["currentScore", "currentSetScore", "currentMatchScore"]
    matchData = pd.DataFrame(columns = column_names)
    MatchScoreL = 0
    MatchScoreR = 0
    gameData = entry
    gameData.append("E")

    SetScore = "0-0"

    def updateMatchScore():  
        if (int(SetScore[0]) > int(SetScore[2])):
            global MatchScoreL
            MatchScoreL += 1
        if (int(SetScore[0]) < int(SetScore[2])):
            global MatchScoreR 
            MatchScoreR += 1


    for token in gameData:
        if "*" in token:   
            matchData_length = len(matchData)
            matchData.loc[matchData_length] = [token,SetScore, str(MatchScoreL) + "-" + str(MatchScoreR)]
        elif token == "E" :
            updateMatchScore()
            matchData_length = len(matchData)
            matchData.loc[matchData_length] = ["EndGame","EndSet", str(MatchScoreL) + "-" + str(MatchScoreR)]
            MatchScoreL = 0
            MatchScoreR = 0
        else:
            if token == "0-0":
                updateMatchScore()
                matchData_length = len(matchData)
                matchData.loc[matchData_length] = ["EndGame",SetScore, str(MatchScoreL) + "-" + str(MatchScoreR)]

            SetScore = token

    return matchData

            


    


