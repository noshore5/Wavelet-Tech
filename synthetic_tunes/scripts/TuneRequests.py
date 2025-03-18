import requests
from TuneClass import *
from keys import *

import pandas as pd

def preprocess_string(input_string):
    ret = input_string.lower().replace('the', '').strip().replace(' ','')
    return ret.replace(',','').replace("'",'')

def find_tune_id(input_value):
    tunefile = 'tune_id.csv'
    input_value = preprocess_string(input_value)
    df = pd.read_csv(tunefile)
    for column in ['alias','name']:
        df[column] = df[column].apply(preprocess_string)
    
    match = df[df[['alias','name']].apply(lambda row: input_value in row.values, axis=1)]  

    return match.iloc[0]['tune_id'] if not match.empty else None

def extract_between(input_string, start_substr, end_substr):
    start_index = input_string.find(start_substr)
    if start_index != -1:
        start_index += len(start_substr)  # Move to the end of the start_substr
        end_index = input_string.find(end_substr, start_index)
        if end_index != -1:
            return input_string[start_index:end_index]
    return ""

import requests

def download_html(url, output_file):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP errors

        # Save the content to a file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(response.text)
        
        #print(f"HTML successfully saved to {output_file}.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def findsetting(setting,filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        starting_junk = ('X:','R:','T:','C','M','S','L','Z','K','<abbr>','</div>','<')
        abc_notation = ""
        settingfound = False
        key = 'Not Found'
        dance = 'Dance not Listed'
        composer = 'Composer Not Listed'
        for line in lines:
            # Look for the title of the tune
            if 'class="setting-abc" id="' in line:# and type(line[48]) == int:
                currentsetting = int(line[48])
                if setting == currentsetting:
                    settingfound = True
                else:
                    settingfound = False
                # need to add in the rest of attributes
            if  line.startswith('<meta name="description" content="'): 
                composer = extract_between(line,'by ',' with')
                if composer == '':
                    composer = 'Composer Not Found'
            if settingfound and line.startswith('<abbr title="Key">K'): 
                key = choose_key(line[28:])
            if settingfound and line.startswith('<abbr title="Type">R</abbr>:'): 
                dance = line[29:]
                index = dance.find('<')
                dance = dance[:index].capitalize()

            if settingfound and not line.startswith(starting_junk):
                abc_notation += line.strip()
            elif settingfound and line.startswith('</div>'):
                break

    return [composer,key,dance,abc_notation.replace('<br','')]

def tuneloader(name,setting):
    """
    Args:
    Just name an Irish Tune
    """
    id = find_tune_id(name)
    if id == None:
        return [0,0,0,0]
        
    url = f"https://www.thesession.org/tunes/{id}"
    output_file = "example.txt"
    download_html(url, output_file)
    return findsetting(setting,'example.txt')