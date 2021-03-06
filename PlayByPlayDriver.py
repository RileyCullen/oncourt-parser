import os, time, re, json, argparse
import pandas as pd

from enum import Enum, auto
from OnCourtDriver import get_file_paths, clean_player_name
from parsers.PlayParser import parse_entry
from progress_bar.ProgressBar import update_progress
from verifiers.PlayVerifier import verify_play_by_play_data
from database.DBConnection import DBConnection
from database.PopulateDB import populate_player_table, \
    populate_in_play_data_table, populate_tournament_table, populate_match_table
from database.ObtainData import get_player_id, get_tournament_id, get_match_id

class ParseMode(Enum):
    XLSX = auto()
    DB   = auto()

def main():
    """
    The entry point for the play-by-play data parser. This function is responsible 
    for verifying the input arguments, in addition to opening the files, calling the
    play-by-play parser, then running the secondary parser on the points data.

    Usage:

    python PlayByPlayDriver.py [input_file/input_path] [output_path]
    """
    try: 
        arg_parser = argparse.ArgumentParser()
        subparser = arg_parser.add_subparsers(help="Write to .xlsx file or \
            database (db)", dest='command')

        # Create arguments for xlsx option
        xlsx_parser = subparser.add_parser('xlsx', help='xlsx help')
        xlsx_parser.add_argument("-i", "--inpath", help="Input path for file \
            that needs to be parsed", required=True, default=None)
        xlsx_parser.add_argument("-o", "--outpath", help="Output path", \
            required=True, default=None)

        # Create arguments for db option
        db_parser = subparser.add_parser('db', help='db help')
        db_parser.add_argument("-i", "--inpath", help="Input path for file \
            that needs to be parsed", required=True, default=None)
        db_parser.add_argument("-u", "--username", help="Username for DB connec\
            tion", required=True, default=None)
        db_parser.add_argument("-p", "--password", help="Password for DB access",
            required=True, default=None)
        db_parser.add_argument("-s", "--server", help="Username for DB connec\
            tion", required=False, default='tennismodelling.database.windows.net')
        db_parser.add_argument("-db", "--database", help="Username for DB connec\
            tion", required=False, default='TennisModelling')
        db_parser.add_argument("-dr", "--driver", help="Username for DB connec\
            tion", required=False, default='{ODBC Driver 17 for SQL Server}')

        args = arg_parser.parse_args()

        mode = None
        run_args = None
        if (args.command == 'xlsx'):
            if (os.path.exists(args.outpath)):
                raise FileNotFoundError(args.outpath + " already exists")
            mode = ParseMode.XLSX
            run_args = (args.outpath,)
        elif (args.command == 'db'):
            mode = ParseMode.DB
            DBConnection().create_connection(args.server, args.database, \
                args.username, args.password, args.driver)
        else:
            raise Exception("Need to specify xlsx or db")
        
        # Check to see if input path exists
        if (not os.path.exists(args.inpath)):
            raise FileNotFoundError(args.inpath + " does not exist")
        run(mode, args.inpath, run_args)

    except SyntaxError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)
    except FileExistsError as e:
        print(e)

    if (mode == ParseMode.DB): DBConnection().close_connection()

def run(mode: ParseMode, input_path: str, args: tuple):
    """
    This function is responsible for finding all the files specified by 'input_path',
    parsing the contents of the file, calling the PlayParser, then processing that
    into a usable format.

    Preconditions:
    --------------
    Note that this function assumes that input_path already exists and that 
    output_path does not exist.

    Parameters:
    -----------
    mode: XLSX or DB 
    input_path:  The input path denoting the file (or folder containing the 
                 files) we want to parse. Note that this can be a single file or
                 a folder containing .xlsl files.
    args: If XLSX, it assumes a tuple = (output_path). If DB it assumes a tuple
          = ().
    """
    files = get_file_paths(input_path)
    # Output - an array of Pandas.DataFrames
    output = []
    log = None
    i = 1
    for file_path in files:
        print("Parsing " + file_path + " (" + str(i) + "/" + str(len(files)) + ")")
        file_contents = open_file(file_path)
        return_data, log = get_play_data(mode, file_contents)
        output.append(return_data)
    
    if (mode == ParseMode.XLSX):
        os.mkdir(args[0])
        for data in output:
            data.to_excel(args[0] +"/out.xlsx", index=False)
            if (log != None and log != []):
                with open(args[0] + "/logs.json", 'w') as f:
                    json.dump(log, f, ensure_ascii=False, indent=4)

def open_file(path: str) -> pd.DataFrame:
    """
    This file is responsible for obtaining the contents of the .xlsx specified 
    by path.

    Parameters:
    -----------
    path: A file path to the .xlsx file we want to parse.

    Return Value: 
    -------------
    This function returns a Pandas.DataFrame containing the contents of the .xlsx
    file we are opening.
    """
    df = pd.read_excel(path, engine='openpyxl', index_col=None, header=None)
    df = df.iloc[1:]
    return df

def get_play_data(mode: ParseMode, df: pd.DataFrame):
    """
    Not exactly sure how this function should work, but the general idea is it
    should:
        1. Obtain the play-by-play data (in addition to other meta data needed 
           from df)
        2. Parse the play-by-play data to write the "usable" data
    
    Parameters:
    -----------
    df: The Pandas.DataFrame containing match info.

    Returns:
    --------
    A Pandas.DataFrame containing usable data obtained from the play parser.
    """
    frames = []
    logs = []
    total_entries = 0

    output_columns = ["Key", "SetNo", "P1GamesWon", "P2GamesWon", "SetWinner", 
        "GameNo", "GameWinner", "PointNumber", "PointWinner", "PointServer", 
        "P1Score", "P2Score", "GameStatus"]

    prev_tournament_name = ""
    tournament_id = -1

    for i, row in df.iterrows():
        # Run PlayParser
        # Call function to parse output of PlayParser
        # Add function output to output DataFrame
        p1_name = clean_player_name(row[0])
        p2_name = clean_player_name(row[1])
        date = str(row[3])[0:10]
        entry_key = p1_name + " " + p2_name + " " + date

        player_one_id = -1
        player_two_id = -1

        match_id = -1

        if (mode == ParseMode.DB):
            conn = DBConnection().get_connection()
            tournament_name = row[2]
            if (prev_tournament_name == "" or prev_tournament_name != tournament_name):
                prev_tournament_name = tournament_name
                populate_tournament_table(conn, tournament_name)
                tournament_id = get_tournament_id(conn, tournament_name)

            populate_player_table(conn, p1_name)
            populate_player_table(conn, p2_name)

            player_one_id = get_player_id(conn, p1_name)
            player_two_id = get_player_id(conn, p2_name)

            populate_match_table(conn, tournament_id, player_one_id, player_two_id)
            match_id = get_match_id(conn, tournament_id, player_one_id, player_two_id)

        if (isinstance(row[15], str) and not re.match("\s+", row[15])):
            df_play = parse_entry(row[15])
            total_entries += len(df_play)
            logs += verify_play_by_play_data(df_play, entry_key)

            if (mode == ParseMode.XLSX):
                output_df = pd.DataFrame(columns=output_columns)
                output_df = output_df.iloc[1:]

                for entry in parse_play_dataframe(df_play, entry_key):
                    output_df = output_df.append(entry, ignore_index=True)

                frames.append(output_df)
            elif (mode == ParseMode.DB):
                conn = DBConnection().get_connection()
                for entry in parse_play_dataframe(df_play, entry_key):
                    populate_in_play_data_table(conn, match_id,
                        entry['SetNo'], entry['P1GamesWon'], 
                        entry['P2GamesWon'], entry['SetWinner'], 
                        entry['GameNo'], entry['GameWinner'], 
                        entry['PointNumber'], entry['PointWinner'],
                        entry['PointServer'], entry['P1Score'], entry['P2Score']
                        , entry['GameStatus'])
        update_progress(i / len(df.index))

    screw_up_score = 1 - (len(logs) / total_entries)
    for entry in logs:
        print(entry)
    print("Data Integrity: " + str(screw_up_score))     

    if frames == []: return [], logs

    return pd.concat(frames), logs

def parse_play_dataframe(df: pd.DataFrame, key: str) -> pd.DataFrame:
    """
    This function is responsible for calculating the following entries using the 
    output from parse_enty in PlayParser.py:
        1. Set number
        2. P1 games won
        3. P2 games won
        4. Set winner
        5. Game number
        6. Game winner
        7. Point number
        8. Point winner
        9. Point server.
    
    Once this data is calculated, it will be output to the user in the form of a
    Pandas.Dataframe.

    Parameters:
    -----------
    df: The Pandas.DataFrame we want to analyze.
    key: The key corresponding to the particular match that it being played.

    Returns:
    --------
    A dictionary containg the above attributes.
    """ 

    set_no = 1
    game_no = 1
    point_no = 0
    point_server = 0
    prev_points = 0

    prev_games_won = '0'

    for i, row in df.iterrows():
        set_games = row[1].split("-")
        if (len(set_games) == 2):
            set_winner = 1 if set_games[0] > prev_games_won else 2
            prev_games_won = set_games[0]

            set_games[0] = set_games[0][0]
            set_games[1] = set_games[1][0]

            if (row[0] == "EndGame"):
                yield {
                    "Key": key,
                    "SetNo": set_no,
                    "P1GamesWon": set_games[0],
                    "P2GamesWon": set_games[1],
                    "SetWinner": 0,
                    "GameNo": game_no,
                    "GameWinner": set_winner,
                    "PointNumber": 0, 
                    "PointWinner": set_winner,
                    "PointServer": point_server,
                    "P1Score": 0,
                    "P2Score": 0,
                    "GameStatus": row[0]
                } 
                game_no += 1
                prev_points = 0
            elif (row[0] == "EndSet" ):
                yield {
                    "Key": key,
                    "SetNo": set_no,
                    "P1GamesWon": set_games[0],
                    "P2GamesWon": set_games[1],
                    "SetWinner": set_winner,
                    "GameNo": game_no,
                    "GameWinner": set_winner,
                    "PointNumber": 0, 
                    "PointWinner": set_winner,
                    "PointServer": point_server,
                    "P1Score": 0,
                    "P2Score": 0,
                    "GameStatus": row[0]
                }
                game_no = 1
                set_no += 1
                prev_points = 0
            elif (row[0] == "End"):
                yield {
                    "Key": key,
                    "SetNo": set_no,
                    "P1GamesWon": set_games[0],
                    "P2GamesWon": set_games[1],
                    "SetWinner": set_winner,
                    "GameNo": game_no,
                    "GameWinner": set_winner,
                    "PointNumber": 0, 
                    "PointWinner": set_winner,
                    "PointServer": point_server,
                    "P1Score": 0,
                    "P2Score": 0,
                    "GameStatus": row[0]
                }
                game_no = 1
                prev_points = 0
            else:
                remove_brackets = row[0].replace("[", "").replace("]", "")
                point_server = 2
                remove_asterisk = remove_brackets.replace("*", "")
                games = remove_asterisk.split("-")

                try:
                    if (remove_brackets.index('*') == 0): point_server = 1
                except ValueError:
                    point_server = -1

                point_winner = 0
                if (prev_points == 0):
                    point_winner = 1 if games[0] > games[1] else 2
                else:
                    if (prev_points[1] == 'A'):
                        point_winner = 2 if games[1] > prev_points[1] else 1
                    else:
                        point_winner = 1 if games[0] > prev_points[0] else 2
                prev_points = games
                yield {
                    "Key": key,
                    "SetNo": set_no,
                    "P1GamesWon": set_games[0],
                    "P2GamesWon": set_games[1],
                    "SetWinner": 0,
                    "GameNo": game_no,
                    "GameWinner": 0,
                    "PointNumber": point_no, 
                    "PointWinner": point_winner,
                    "PointServer": point_server,
                    "P1Score": games[0],
                    "P2Score": games[1],
                    "GameStatus": 'In-progress'
                }
                point_no += 1

if __name__ == "__main__":
    start = time.time()
    main()
    print("Elapsed time: " + str(time.time() - start))