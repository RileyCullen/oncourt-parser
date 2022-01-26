import pandas as pd

def parse_entry(entry):
    """
    Desc: Given a string, parse it by spliting element separated by spaces into
          different column elements and the groups separated by |'s into 
          different rows.
    Parameters:
    ---------------
    entry: string
    Returns:
    ---------------
    Returns a Pandas.DataFrame containing the parsed information.
    """
    if (not isinstance(entry, str)): return pd.DataFrame()
    tokens = tokenize(entry)
    df = pd.DataFrame(columns=['Date', 'Time', 'P1-odds', 'P2-odds', 'P1-Handicap',
    'P1-Handicap-Odds', 'P2-Handicap', 'P2-Handicap-Odds', 'Game-Pred', 
        'Odds-under', 'Odds-over'])
    for token in tokens:
        cleaned_data = remove_empty_entries(token)
        data_len = len(cleaned_data)
        if (data_len != 0):
            if (data_len == 4):
                df = df.append({
                    'Date': cleaned_data[0],
                    'Time': cleaned_data[1],
                    'P1-odds': cleaned_data[2],
                    'P2-odds': cleaned_data[3],
                    'P1-Handicap': 'N/A',
                    'P1-Handicap-Odds': 'N/A',
                    'P2-Handicap': 'N/A',
                    'P2-Handicap-Odds': 'N/A',
                    'Game-Pred': 'N/A',
                    'Odds-under': 'N/A',
                    'Odds-over': 'N/A',
                }, ignore_index=True)
            elif (data_len == 7):
                df = df.append({
                    'Date': cleaned_data[0],
                    'Time': cleaned_data[1],
                    'P1-odds': cleaned_data[2],
                    'P2-odds': cleaned_data[3],
                    'P1-Handicap': 'N/A',
                    'P1-Handicap-Odds': 'N/A',
                    'P2-Handicap': 'N/A',
                    'P2-Handicap-Odds': 'N/A',
                    'Game-Pred': cleaned_data[4],
                    'Odds-under': cleaned_data[5],
                    'Odds-over': cleaned_data[6],
                }, ignore_index=True) 
            else:
                df = df.append({
                    'Date': cleaned_data[0],
                    'Time': cleaned_data[1],
                    'P1-odds': cleaned_data[2],
                    'P2-odds': cleaned_data[3],
                    'P1-Handicap': cleaned_data[4] if data_len == 11 else 'N/A',
                    'P1-Handicap-Odds': cleaned_data[5] if data_len == 11 else 'N/A',
                    'P2-Handicap': cleaned_data[6] if data_len == 11 else 'N/A',
                    'P2-Handicap-Odds': cleaned_data[7] if data_len == 11 else 'N/A',
                    'Game-Pred': cleaned_data[5 if data_len == 8 else 8],
                    'Odds-under': cleaned_data[6 if data_len == 8 else 9],
                    'Odds-over': cleaned_data[7 if data_len == 8 else 10],
                }, ignore_index=True)
    return df

def tokenize(str):
    """
    Desc: Tokenize the string, first spliting by '|' then splitting by spaces.
    Parameters:
    ---------------
    str: string
    Returns:
    ---------------
    A multidimensional array. 
    [token1, token2, token3, etc] where token1 through tokenN are tokens separated
    by '|' and tokenN = [token1a, token1b, etc] where these are the tokens
    split by spaces.
    """
    return_list = []
    split_one = str.split('|')
    for token in split_one:
        return_list.append(token.split(' '))
    return return_list

def remove_empty_entries(input_list):
    """
    Desc: Remove all of the empty entries in input_list.
    Parameters:
    ---------------
    input_list: list
    Returns:
    ---------------
    A list with all of the empty('') entries removed.
    """
    tmp_list = []
    for elem in input_list:
        if (elem != ''):
            tmp_list.append(elem)
    return tmp_list