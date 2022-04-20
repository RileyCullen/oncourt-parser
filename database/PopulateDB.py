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

def populate_in_play_data_table(conn, Key,SetNo,P1GamesWon,P2GamesWon,SetWinner,GameNo,GameWinner,PointNumber,PointWinner,PointServer,Score):
    """
    This function populates the IN_PLAY_DATA table of the Azure SQL Database

    Parameters:
    -----------
    conn: see populate_player_table
    """
    cursor = conn.cursor()
    sqlInsert = "INSERT INTO [IN_PLAY_DATA]([IN_PLAY_DATA_KEY], [IN_PLAY_DATA_SET_NUMBER], [IN_PLAY_DATA_PLAYER_ONE_GAMES_WON], [IN_PLAY_DATA_PLAYER_TWO_GAMES_WON],[IN_PLAY_DATA_SET_WINNER],"\
                  +"[IN_PLAY_DATA_GAME_NUMBER], [IN_PLAY_DATA_GAME_WINNER], [IN_PLAY_DATA_POINT_NUMBER], [IN_PLAY_DATA_POINT_WINNER], [IN_PLAY_DATA_POINT_SERVER],[IN_PLAY_DATA_SCORE]) "\
                  +"VALUES(?,?,?,?,?,?,?,?,?,?,?)"
    parameters = (Key,SetNo,P1GamesWon,P2GamesWon,SetWinner,GameNo,GameWinner,PointNumber,PointWinner,PointServer,Score)
    cursor.execute(sqlInsert, parameters)
    
    conn.commit()