import os, sys, json
import pandas as pd
from parsers.OddsParser import parse_entry
from progress_bar.ProgressBar import update_progress

def main():
    """
    The entry point for the OnCourt data parser, this function is responsible 
    for verifying the input arguments, in addition to opening the files and 
    calling the respective parser. 

    While not explict parameters, main() requires two command line arguments to 
    be specified, the first is the input directory (which must exist) and the 
    output directory (which should not exist).
    """
    try:
        # Check to make sure the proper arguments were given
        if (len(sys.argv) != 3): 
            raise SyntaxError("Invalid input arguments. Input command should \
                be: python OnCourtDriver.py [input directory] [output directory")

        # Check to make sure input directory exists and the output directory does
        # not exist
        if (not os.path.exists(sys.argv[1])): 
            raise FileNotFoundError(sys.argv[1] + " does not exist")
        if (os.path.exists(sys.argv[2])):
            raise FileExistsError(sys.argv[2] + " already exists")
        run(sys.argv[1], sys.argv[2])
    except SyntaxError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)
    except FileExistsError as e:
        print(e)

def run(input_path: str, output_path: str):
    """
    This function is reponsible for finding all the files specified by 'input_path',
    parsing the contents of the file, and writing the collected data to the 
    local file system.

    Preconditions:
    --------------
    Note that this function assumes that input_path already exists and that 
    output_path does not exist.

    Parameters:
    -----------
    input_path:  The input path denoting the file (or folder containing the 
                 files) we want to parse. Note that this can be a single file or
                 a folder containing .xlsl files.
    output_path: The output path where we plan on storing the collected data.
    """
    files = get_file_paths(input_path)
    data_list = []
    for file_path in files:
        data_list.append(parse_file(file_path))
    
    os.mkdir(output_path)
    for data_entry in data_list:
        with open(output_path + '/tmp' + '.json', 'w') as fp:
            json.dump(data_entry, fp, indent=4, ensure_ascii=True)


def get_file_paths(input_path: str) -> list:
    """
    This function is reponsible for obtaining all the .xlsl files specified by
    input_path.

    Parameters:
    -----------
    input_path: see run() documentation.

    Return Value:
    -------------
    Returns a list containing all of the .xlsl files to the calling function.
    """
    if (os.path.isfile(input_path)):
        return [input_path]
    else:
        return os.listdir(input_path)

def parse_file(path: str) -> dict:
    """
    This function is responsible for parsing the .xlsx file specified by path.

    Preconditions:
    --------------
    This function assumes that the file defined by path exists and is formatted
    as specified by the OnCourt dataset standards.

    Parameters:
    -----------
    path: A file path to the .xlsx file we want to parse.

    Return Value: 
    -------------
    This function returns a dictionary with containing the collected data in 
    path.
    """

    # Read excel file and store in Pandas.DataFrame
    df = pd.read_excel(path, engine='openpyxl', index_col=None, header=None)

    # Remove first row (the header)
    df = df.iloc[1:]

    file_data = {}

    for i, row in df.iterrows():
        tournament_key = row[2]
        if tournament_key in file_data.keys():
            entry_key = row[0] + ' ' + row[1] + ' ' + str(row[3])
            tmp_entry = {
                "p1_name": row[0],
                "p2_name": row[1],
                "date": str(row[3]),
                "odds": parse_entry(row[14]).to_json()
            }
            file_data[tournament_key]["match_data"][entry_key] = tmp_entry
        else:
            file_data[tournament_key] = {
                "match_data": {}
            }
        update_progress(i / len(df.index))
    return file_data

if __name__ == "__main__":
    main()