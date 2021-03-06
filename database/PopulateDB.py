def populate_tournament_table(conn, tournament_name: str) -> None:
    """
    This function adds a tournament to the tournament table.
    """

    sql = "INSERT INTO [TOURNAMENT](TOURNAMENT_NAME)" + \
        "VALUES(?)" + \
        "WHERE NOT EXISTS (SELECT [TOURNAMENT_ID] FROM [TOURNAMENT] WHERE [TOURNAMENT_NAME] = (?))"
    parameters = (tournament_name)

    cursor = conn.cursor()
    cursor.execute(sql, parameters)
    conn.commit()

def populate_match_table(conn, tournament_id, player_one_id, player_two_id):
    """
    This function adds a match to the match table.
    """

    sql = "INSERT INTO [MATCH](TOURNAMENT_ID, PLAYER_ID_ONE, PLAYER_ID_TWO" + \
        "VALUES(?, ?, ?)"
    parameters = (tournament_id, player_one_id, player_two_id)

    cursor = conn.cursor()
    cursor.execute(sql, parameters)
    conn.commit()

def populate_player_table(conn, PlayerName):
    """
    This function populates the PLAYER table.

    Parameters:
    -----------
    conn: pyodbc connection object.
    """
    sql = "EXEC [TennisModelling].[dbo].[SP_PLAYER_NAME_ADD] ?"
    cursor = conn.cursor()
    #sqlInsert = "INSERT INTO [PLAYER]([PLAYER_NAME]) " \
    #            "VALUES(?)" \
    #            "WHERE NOT EXISTS (SELECT [PLAYER_ID] FROM [PLAYER] WHERE [PLAYER_NAME] = (?)"
    parameters = (PlayerName)
    cursor.execute(sql, parameters)
    conn.commit()

def populate_in_play_data_table(conn, Key,SetNo,P1GamesWon,P2GamesWon,SetWinner,GameNo,GameWinner,PointNumber,PointWinner,PointServer,P1Score, P2Score, status):
    """
    This function populates the IN_PLAY_DATA table of the Azure SQL Database

    Parameters:
    -----------
    conn: see populate_player_table
    """
    cursor = conn.cursor()
    sqlInsert = "INSERT INTO [IN_PLAY_DATA]([IN_PLAY_DATA_KEY], [SET_NUMBER], [PLAYER_ONE_GAMES_WON], [PLAYER_TWO_GAMES_WON], [SET_WINNER],"\
                  +"[GAME_NUMBER], [GAME_WINNER], [POINT_NUMBER], [POINT_WINNER], [POINT_SERVER],[PLAYER_ONE_SCORE], [PLAYER_TWO_SCORE], [GAME_STATUS]) "\
                  +"VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"
    parameters = (Key,SetNo,P1GamesWon,P2GamesWon,SetWinner,GameNo,GameWinner, \
        PointNumber,PointWinner,PointServer, P1Score, P2Score, status)
    cursor.execute(sqlInsert, parameters)
    
    conn.commit()