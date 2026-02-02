import requests
import pandas as pd

def fetch_nhl_points_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/hockey/nhl/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][2]['leaders']

    # set up the dataframe:
    points_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        'Points': leader['displayValue']
    }
    for leader in leaders                        
    )

    points_df.index = range(1, len(points_df) + 1)
    return points_df

def fetch_nhl_goals_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/hockey/nhl/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][0]['leaders']

    # set up the dataframe:
    goals_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        'Goals': leader['displayValue']
    }
    for leader in leaders                        
    )

    goals_df.index = range(1, len(goals_df) + 1)
    return goals_df

def fetch_nhl_assists_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/hockey/nhl/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][1]['leaders']

    # set up the dataframe:
    assists_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        'Assists': leader['displayValue']
    }
    for leader in leaders                        
    )

    assists_df.index = range(1, len(assists_df) + 1)
    return assists_df

def fetch_nhl_plus_minus_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/hockey/nhl/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][3]['leaders']

    # set up the dataframe:
    plus_minus_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        '+/-': leader['displayValue']
    }
    for leader in leaders                        
    )

    plus_minus_df.index = range(1, len(plus_minus_df) + 1)
    return plus_minus_df

def fetch_nhl_gaa_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/hockey/nhl/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][4]['leaders']

    # set up the dataframe:
    gaa_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        'GAA': leader['displayValue']
    }
    for leader in leaders                        
    )

    gaa_df.index = range(1, len(gaa_df) + 1)
    return gaa_df

def fetch_nhl_pim_leaders():
    url = "https://site.api.espn.com/apis/site/v3/sports/hockey/nhl/leaders"

    response = requests.get(url)
    data = response.json()

    leaders = data['leaders']['categories'][5]['leaders']

    # set up the dataframe:
    pim_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['team']['displayName'],
        'PIM': leader['displayValue']
    }
    for leader in leaders                        
    )

    pim_df.index = range(1, len(pim_df) + 1)
    return pim_df