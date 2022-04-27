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

    total_p1 = 0
    total_p2 = 0

    # Get only in-progress status entries
    df = df[df['GameStatus'] == 'In-progress']

    updated_df = pd.DataFrame(columns=["P1", "P2"])

    for i, row in df.iterrows():
        if (row[8] == 1):
            if (row[10] == 'A'): total_p1 += 5 
            else: total_p1 += int(row[10])
        elif (row[8] == 2): 
            if (row[11] == 'A'): total_p2 += 5
            else: total_p2 += int(row[11])
    
        updated_df = updated_df.append({
            "P1": total_p1,
            "P2": total_p2,
        }, ignore_index = True)

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

if __name__ == '__main__':
    main()