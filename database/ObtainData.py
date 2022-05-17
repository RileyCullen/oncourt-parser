def get_tournament_id(conn, tournament_name):
    sql = "SELECT [TOURNAMENT_ID]" + \
        "FROM [TOURNAMENT]" + \
        "WHERE [TOURNAMENT_NAME] = (?)"
    parameters = (tournament_name)

    cursor = conn.cursor()
    cursor.execute(sql, parameters)
    return cursor.fetchall()[0]

def get_player_id(conn, player_name):
    sql = "SELECT [PLAYER_ID]" + \
        "FROM [PLAYER]" + \
        "WHERE [PLAYER_NAME] = (?)"
    parameters = (player_name)

    cursor = conn.cursor()
    cursor.execute(sql, parameters)
    return cursor.fetchall()[0]

def get_match_id(conn, tournament_id, p1_id, p2_id):
    sql = "SELECT [MATCH_ID]" + \
        "FROM [MATCH]" + \
        "WHERE [TOURNAMENT_ID] = (?) [PLAYER_ID_ONE] = (?) AND [PLAYER_ID_TWO] = (?)"
    parameters = (tournament_id, p1_id, p2_id)
    cursor = conn.cursor()
    cursor.execute(sql, parameters)
    return cursor.fetchall()[0]