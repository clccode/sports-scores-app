import requests
import pandas as pd

url = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/statistics"

def get_pl_season_type():
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        season_type = data['season']['displayName']
        return season_type
    except Exception as e:
        print(f"Error fetching Premier League season type: {e}")
        return "Season"

def fetch_pl_goal_leaders():
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        goals_leaders = data['stats'][0]['leaders']
        goals_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['athlete']['team']['displayName'],
        'Matches Played': leader['athlete']['statistics'][0]['displayValue'],
        'Goals': leader['athlete']['statistics'][1]['displayValue'],
        }
        for leader in goals_leaders                        
        )

        # Add ranks to the data frame
        goals_df['Goals'] = goals_df['Goals'].astype(int)
        goals_df['Rank'] = goals_df['Goals'].rank(method='min', ascending=False).astype(int)

        # Sort by rank
        goals_df = goals_df.sort_values('Rank')

        # Create display rank - show rank only for first occurrence of each rank
        goals_df['Display_Rank'] = goals_df['Rank'].where(
            goals_df['Rank'] != goals_df['Rank'].shift(),
            ''
        ).astype(str)

        # Set Display_Rank as index
        goals_df = goals_df.set_index('Display_Rank')
        goals_df.index.name = 'Rank'

        # Drop the original Rank column since it's now in the index
        goals_df = goals_df.drop('Rank', axis=1)
        goals_df['Goals'] = goals_df['Goals'].astype(str)
        return goals_df
    except Exception as e:
        print(f"Error fetching Premier League goal leaders: {e}")
        return None, pd.DataFrame()
    
def fetch_pl_assist_leaders():
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        assist_leaders = data['stats'][1]['leaders']
        assist_df = pd.DataFrame({
        'Player': leader['athlete']['displayName'],
        'Team': leader['athlete']['team']['displayName'],
        'Matches Played': leader['athlete']['statistics'][0]['displayValue'],
        'Assists': leader['athlete']['statistics'][2]['displayValue'],
        }
        for leader in assist_leaders                        
        )

        # Add ranks to the data frame
        assist_df['Assists'] = assist_df['Assists'].astype(int)
        assist_df['Rank'] = assist_df['Assists'].rank(method='min', ascending=False).astype(int)

        # Sort by rank
        assist_df = assist_df.sort_values('Rank')

        # Create display rank - show rank only for first occurrence of each rank
        assist_df['Display_Rank'] = assist_df['Rank'].where(
            assist_df['Rank'] != assist_df['Rank'].shift(),
            ''
        ).astype(str)

        # Set Display_Rank as index
        assist_df = assist_df.set_index('Display_Rank')
        assist_df.index.name = 'Rank'

        # Drop the original Rank column since it's now in the index
        assist_df = assist_df.drop('Rank', axis=1)
        assist_df['Assists'] = assist_df['Assists'].astype(str)

        return assist_df
    except Exception as e:
        print(f"Error fetching Premier League assist leaders: {e}")
        return None, pd.DataFrame()
        