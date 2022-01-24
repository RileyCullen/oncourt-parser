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

if __name__ == "__main__":
    main()