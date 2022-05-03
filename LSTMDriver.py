import argparse, os
import pandas as pd

from OnCourtDriver import get_file_paths

def main():
    """
    The purpose of this script is to read output files from the PlayByPlayDriver
    and convert them into an LSTM compatible format. In other words, files 
    written from this driver will contain four columns:

    1. P1 Given 
    2. P1 Expected
    3. P2 Given
    4. P2 Expected 
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i', '--inpath', help='Input path', required=True)
    arg_parser.add_argument('-o', '--outpath', help='Output folder', required=True)
    args = arg_parser.parse_args()

    try:
        if (not os.path.exists(args.inpath)):
            raise FileNotFoundError(args.inpath + " does not exist.")
        if (os.path.exists(args.outpath)):
            raise FileExistsError(args.outpath + " already exists.")

        run(args.inpath, args.outpath)
    except FileNotFoundError as e:
        print(e)
    except FileExistsError as e:
        print(e)

def run(input_path: str, output_path: str):
    files = get_file_paths(input_path)

    output = []
    for path in files:
        df = pd.read_excel(path, engine='openpyxl', index_col=None)
        game_list = separate_games(df)
        for game_df in game_list:
            output.append(convert(game_df))
    
    os.mkdir(output_path)

    i = 0
    for file in output:
        file.to_excel(output_path + '/' + str(i) + '.xlsx', index=False)

def separate_games(df: pd.DataFrame) -> list:
    """
    Separates the games in df into multiple pd.DataFrame types. These DataFrames
    are stored in a list and returned to the caller.
    """
    keys = df.Key.unique()
    tmp = []

    for key in keys:
        tmp.append(df[df['Key'] == key])
    return tmp

def convert(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert df to format listed in main's documentation.
    """
    tmp_df = pd.DataFrame(columns=["P1_Given", "P1_Expected", "P2_Given", "P2_Expected"])
    
    updated_df = create_modified_df(df)
    
    prev = None
    prev_toggle = False

    for i, row in updated_df.iterrows():
        if (prev_toggle):
            tmp_df = tmp_df.append({
                'P1_Given': prev[0],
                'P1_Expected': row[0],
                'P2_Given': prev[1],
                'P2_Expected': row[1],
            }, ignore_index=True)
        else: prev_toggle = True
        prev = row
    return tmp_df

def create_modified_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Given a dataframe with the same layout as the output from the PlayByPlay
    driver, convert it to a dataframe that adheres to the following rules:
        1. There exists two columns, P1 and P2, such that P1 represents player
           one's cumulative score at a given serve and P2 represents player 
           two's cumulative score at a given serve.
        2. Cumulative scores will be calculated by taking the difference 
           between the last score and the current score.
        3. In the case of an advantage (A), a fixed value of 5 will be added
           for each "A" entry.
    """
    WINNER = 50
    ADV = 5

    final_df = pd.DataFrame(columns=["P1", "P2"])
    prev_score_p1 = 0
    prev_score_p2 = 0

    total_p1 = 0
    total_p2 = 0

    for i, row in df.iterrows():
        if (row[12] == 'In-progress'):
            if (row[8] == 1):
                if (row[10] == 'A'): total_p1 += ADV
                elif (prev_score_p2 == 'A'): total_p1 += ADV 
                else: total_p1 += (int(row[10]) - int(prev_score_p1))
            elif (row[8] == 2):
                if (row[11] == 'A'): total_p2 += ADV
                elif (prev_score_p1 == 'A'): total_p2 += ADV
                else: total_p2 += (int(row[11]) - int(prev_score_p2))

            prev_score_p1 = row[10] 
            prev_score_p2 = row[11]
        else:
            prev_score_p1 = 0
            prev_score_p2 = 0

            if (row[6] == 1):
                total_p1 += WINNER
                total_p2 -= WINNER
            else:
                total_p1 -= WINNER
                total_p2 += WINNER
        
        final_df = final_df.append({
            'P1': total_p1,
            'P2': total_p2
        }, ignore_index=True)

    return final_df

if __name__ == '__main__':
    main()