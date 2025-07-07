import sqlite3
import pandas as pd
from TuneRequests import *

# Connect to the database
conn = sqlite3.connect('thesession.db')

# Load a table into a pandas DataFrame
tunes = pd.read_sql_query("SELECT * FROM tunes", conn)

aliases = pd.read_sql_query("SELECT * FROM aliases", conn)

# Close the connection
conn.close()

# will preprocess string before feeding it into initializer
def initializer(name,setting):
    name = preprocess_string(name)
    # should return lowest setting, can request higher settings later
    matched = tunes[tunes['name'].apply(preprocess_string) == name]
    if matched.empty == False:
        matched = matched.set_index('setting_id')
        matched.index = range(1,len(matched)+1)
        return matched.loc[setting], len(matched)
    else:
        id = int(aliases[aliases['alias'].apply(preprocess_string) == name]['tune_id'].iloc[0])
        matched = tunes[tunes['tune_id'] == str(id)]
        matched.index = range(1,len(matched)+1)

        return matched.loc[setting], len(matched)

def get_abc(name,setting):
    matched = tunes[tunes['name'] == name]
    matched = matched.set_index('setting_id')
    matched.index = range(1,len(matched)+1)

    return [matched['abc'][setting],matched['mode'][setting]]

