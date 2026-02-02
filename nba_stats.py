import requests
import pandas as pd

def fetch_nba_ppg_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/basketball/nba/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][0]['leaders']

    # set up the dataframe:
    ppg_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        'PPG': leader['displayValue']
    }
    for leader in leaders                        
    )

    ppg_df.index = range(1, len(ppg_df) + 1)
    return ppg_df

def fetch_nba_assists_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/basketball/nba/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][1]['leaders']

    # set up the dataframe:
    assists_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        'APG': leader['displayValue']
    }
    for leader in leaders                        
    )

    assists_df.index = range(1, len(assists_df) + 1)
    return assists_df

def fetch_nba_fgp_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/basketball/nba/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][2]['leaders']

    # set up the dataframe:
    fgp_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        'FG%': leader['displayValue']
    }
    for leader in leaders                        
    )

    fgp_df.index = range(1, len(fgp_df) + 1)
    return fgp_df

def fetch_nba_rebounds_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/basketball/nba/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][3]['leaders']

    # set up the dataframe:
    rebounds_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        'RPG': leader['displayValue']
    }
    for leader in leaders                        
    )

    rebounds_df.index = range(1, len(rebounds_df) + 1)
    return rebounds_df

def fetch_nba_ftp_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/basketball/nba/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][6]['leaders']

    # set up the dataframe:
    rebounds_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        'FTP': leader['displayValue']
    }
    for leader in leaders                        
    )

    rebounds_df.index = range(1, len(rebounds_df) + 1)
    return rebounds_df

def fetch_nba_3pt_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/basketball/nba/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][7]['leaders']

    # set up the dataframe:
    threept_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        '3PT%': leader['displayValue']
    }
    for leader in leaders                        
    )

    threept_df.index = range(1, len(threept_df) + 1)
    return threept_df

def fetch_nba_steals_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/basketball/nba/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][4]['leaders']

    # set up the dataframe:
    steals_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        'SPG': leader['displayValue']
    }
    for leader in leaders                        
    )

    steals_df.index = range(1, len(steals_df) + 1)
    return steals_df