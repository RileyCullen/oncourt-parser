# Description 
This program is designed to read through tennis data in the OnCourt dataset and convert the raw data into usable data that can then be queried.
# Getting Started
## Dependencies
This program runs in Python (version 3.8.1 or above) and requires the following depedencies:
1. Pandas
2. NumPy.
Both of these dependecies can be installed using pip, or any other package manager you prefer. For installation instructions, see each individual package's page.
## Running the Program
To run the program, make sure you are in the directory where the driver script resides. Then, in the terminal (or command line), enter `python OnCourtParser [input path] [output path]`. This will then cause the driver to open all the of the files specified by [input path] and then output the cleaned data as a json file to [output path]. Note that [output path] should be unique (i.e. it does not already exist).
