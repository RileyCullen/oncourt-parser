import os, sys

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
        if (len(sys.argv) != 2): 
            raise SyntaxError("Invalid input arguments. Input command should \
                be: python OnCourtDriver.py [input directory] [output directory")

        # Check to make sure input directory exists and the output directory does
        # not exist
        if (not os.path.exists(sys.argv[1])): 
            raise FileNotFoundError(sys.argv[1] + " does not exist")
        if (os.path.exists(sys.argv[2])):
            raise FileExistsError(sys.argv[2] + " already exists")
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
    pass

if __name__ == "__main__":
    main()