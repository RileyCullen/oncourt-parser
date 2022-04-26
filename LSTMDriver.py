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
    tmp_df = pd.DataFrame(columns=["P1_Given", "P1_Expected", "P2_Given", "P2_Expected"])

    total_p1 = 0
    total_p2 = 0

    # Get only in-progress status entries
    df = df[df['GameStatus'] == 'In-progress']

    prev = None
    prev_toggle = False
    
    for i, row in df.iterrows():
        if (prev_toggle):
            given = get_scores(prev)
            expected = get_scores(row)
            tmp_df = tmp_df.append({
                'P1_Given': given[0],
                'P1_Expected': expected[0],
                'P2_Given': given[1],
                'P2_Expected': expected[1],
            }, ignore_index=True)
        else: prev_toggle = True
        prev = row
    return tmp_df

def get_scores(row: tuple) -> tuple:
    return row[10], row[11]

if __name__ == '__main__':
    main()