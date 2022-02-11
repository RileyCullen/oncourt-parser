import pandas as pd






def parse_entry(entry):

    column_names = ["currentScore", "currentSetScore", "currentMatchScore"]
    matchData = pd.DataFrame(columns = column_names)

    gameData = entry.split(" ")
    gameData.append("E")
    MatchScoreL = 0
    MatchScoreR = 0
    SetScore = "0-0"
    


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

    print(matchData.to_string())
    
    return matchData

            
entry = "0-0 [*0-0] [*15-0] [*15-15] [*15-30] [*15-40] [*30-40] 0-1 [0-0*] [15-0*] [15-15*] [15-30*] [15-40*] [30-40*] 0-2 [*0-0] [*15-0] [*30-0] [*30-15] [*40-15] [*40-30] [*40-40] [*A-40] 1-2 [0-0*] [15-0*] [15-15*] [15-30*] [15-40*] 1-3 [*0-0] [*15-0] [*30-0] [*40-0] 2-3 [0-0*] [0-15*] [15-15*] [15-30*] [30-30*] [40-30*] 3-3 [*0-0] [*0-15] [*0-30] [*0-40] 3-4 [0-0*] [15-0*] [15-15*] [15-30*] [15-40*] 3-5 [*0-0] [*15-0] [*15-15] [*30-15] [*40-15] [*40-30] [*40-40] [*A-40] 4-5 [0-0*] [0-15*] [15-15*] [15-30*] [15-40*] 4-6 0-0 [*0-0] [*0-15] [*0-30] [*0-40] 4-6 0-1 [0-0*] [0-15*] [0-30*] [0-40*] 4-6 0-2 [*0-0] [*0-15] [*15-15] [*30-15] [*40-15] [*40-30] 4-6 1-2 [0-0*] [0-15*] [0-30*] [15-30*] [30-30*] [40-30*] [40-40*] [A-40*] [40-40*] [A-40*] 4-6 2-2 [*0-0] [*0-15] [*15-15] [*30-15] [*30-30] [*30-40] 4-6 2-3 [0-0*] [0-15*] [0-30*] [0-40*] 4-6 2-4 [*0-0] [*0-15] [*15-15] [*30-15] [*40-15] 4-6 3-4 [0-0*] [0-15*] [15-15*] [15-30*] [30-30*] [40-30*] [40-40*] [40-A*] 4-6 3-5 [*0-0] [*0-15] [*15-15] [*30-15] [*40-15] [*40-30] [*40-40] [*A-40] 4-6 4-5 [0-0*] [15-0*] [30-0*] [40-0*] 4-6 5-5 [*0-0] [*15-0] [*30-0] [*40-0] 4-6 6-5 [0-0*] [15-0*] [30-0*] [40-0*] [40-15*]"
parse_entry(entry)





