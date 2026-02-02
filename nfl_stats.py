import requests
import pandas as pd

def fetch_nfl_passing_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/football/nfl/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][0]['leaders']

    # set up the dataframe:
    passing_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        'Yards': leader['displayValue']
    }
    for leader in leaders                        
    )

    passing_df.index = range(1, len(passing_df) + 1)
    return passing_df

def fetch_nfl_rushing_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/football/nfl/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][1]['leaders']

    # set up the dataframe:
    rushing_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        'Yards': leader['displayValue']
    }
    for leader in leaders                        
    )

    rushing_df.index = range(1, len(rushing_df) + 1)
    return rushing_df

def fetch_nfl_receiving_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/football/nfl/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][2]['leaders']

    # set up the dataframe:
    receiving_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        'Yards': leader['displayValue']
    }
    for leader in leaders                        
    )

    receiving_df.index = range(1, len(receiving_df) + 1)
    return receiving_df

def fetch_nfl_tackles_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/football/nfl/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][3]['leaders']

    # set up the dataframe:
    tackles_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        'Tackles': leader['displayValue']
    }
    for leader in leaders                        
    )

    tackles_df.index = range(1, len(tackles_df) + 1)
    return tackles_df

def fetch_nfl_sacks_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/football/nfl/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][4]['leaders']

    # set up the dataframe:
    sacks_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        'Sacks': leader['displayValue']
    }
    for leader in leaders                        
    )

    sacks_df.index = range(1, len(sacks_df) + 1)
    return sacks_df