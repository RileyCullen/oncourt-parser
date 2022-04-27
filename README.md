# Description 
This program is designed to read through tennis data in the OnCourt dataset and convert the raw data into usable data that can then be queried.
## OnCourt Driver
The OnCourt driver is responsible for parsing files in the OnCourt dataset and obtaining all data points stored in the file. This data is then stored in a .json file.
## PlayByPlay Driver
The PlayByPlay driver is responsible for parsing through the play-by-play data found in the OnCourt dataset and creating usable data from it. This data is then stored in a .xlsx file. 
# Getting Started
## Dependencies
This program runs in Python (version 3.8.1 or above) and requires the following depedencies:
1. Pandas
2. NumPy
3. pyodbc

Both of these dependecies can be installed using pip, or any other package manager you prefer. For installation instructions, see each individual package's page.
## Running the Program
### OnCourt Driver
To run the program, make sure you are in the directory where the driver script resides. Then, in the terminal (or command line), enter `python OnCourtDriver.py [input path] [output folder]`. This will then cause the driver to open all the of the files specified by [input path] and then output the cleaned data as a json file to [output path]. Note that [output path] should be unique (i.e. it does not already exist).
### PlayByPlay Driver
The PlayByPlay driver is responsible for obtaining play-by-play data from a given match. This script has the option to write to the local disk as an excel (.xlsx) file or write to a database. For instructions on how to run this script, enter into the command line `python PlayByPlayDriver.py -h`.
### LSTM Driver
The LSTMDriver is responsible for converting output from the PlayByPlayDriver into an LSTM compatible format. To run this script, entry into the command line `python LSTMDriver.py -i [input path] -o [output path]`.
