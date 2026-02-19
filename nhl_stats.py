import requests
import pandas as pd

# Cache for API data to avoid multiple calls
_nhl_data_cache = None
_nhl_season_type = None

def _fetch_nhl_data():
    """Fetch NHL leaders data from ESPN API with error handling."""
    global _nhl_data_cache, _nhl_season_type

    if _nhl_data_cache is not None:
        return _nhl_data_cache

    url = "https://site.api.espn.com/apis/site/v3/sports/hockey/nhl/leaders"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        _nhl_data_cache = data['leaders']['categories']
        _nhl_season_type = data['currentSeason']['type']['name']
        return _nhl_data_cache
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Error fetching NHL data: {e}")
        return None

def get_nhl_season_type():
    """Get the current NHL season type (Regular Season, Postseason, etc.)."""
    if _nhl_season_type is not None:
        return _nhl_season_type

    # Fetch data to populate cache if not already done
    _fetch_nhl_data()
    return _nhl_season_type if _nhl_season_type else "Season"

def _build_leaders_df(leaders, stat_column_name):
    """Helper function to build a DataFrame from leaders data."""
    if not leaders:
        return pd.DataFrame()

    try:
        df = pd.DataFrame({
            'Player': [leader['athlete']['displayName'] for leader in leaders],
            'Team': [leader['team']['displayName'] for leader in leaders],
            stat_column_name: [leader['displayValue'] for leader in leaders]
        })

        # Calculate rank (make an exception for GAA where lower is better)
        numeric_col = pd.to_numeric(df[stat_column_name], errors='coerce')
        if stat_column_name == 'GAA':
            df['Rank'] = numeric_col.rank(method='min', ascending=True).astype(int)
        else:
            df['Rank'] = numeric_col.rank(method='min', ascending=False).astype(int)

        # sort by rank
        df = df.sort_values('Rank')

        #Create display rank with "T" for ties
        # Check if current rank appears more than once (is tied)
        rank_counts = df['Rank'].value_counts()
        df['Display_Rank'] = df['Rank'].apply(
            lambda rank: f"T{rank}" if rank_counts[rank] > 1 else str(rank)
        )
        # Set Display_Rank as index
        df = df.set_index('Display_Rank')
        df.index.name = 'Rank'

        # Drop the numeric Rank column
        df = df.drop('Rank', axis=1)
        return df
    except (KeyError, TypeError) as e:
        print(f"Error building DataFrame: {e}")
        return pd.DataFrame()

def fetch_nhl_points_leaders():
    categories = _fetch_nhl_data()
    if categories is None or len(categories) < 3:
        return pd.DataFrame()
    return _build_leaders_df(categories[2]['leaders'], 'Points')

def fetch_nhl_goals_leaders():
    categories = _fetch_nhl_data()
    if categories is None or len(categories) < 1:
        return pd.DataFrame()
    return _build_leaders_df(categories[0]['leaders'], 'Goals')

def fetch_nhl_assists_leaders():
    categories = _fetch_nhl_data()
    if categories is None or len(categories) < 2:
        return pd.DataFrame()
    return _build_leaders_df(categories[1]['leaders'], 'Assists')

def fetch_nhl_plus_minus_leaders():
    categories = _fetch_nhl_data()
    if categories is None or len(categories) < 4:
        return pd.DataFrame()
    return _build_leaders_df(categories[3]['leaders'], '+/-')

def fetch_nhl_gaa_leaders():
    categories = _fetch_nhl_data()
    if categories is None or len(categories) < 5:
        return pd.DataFrame()
    return _build_leaders_df(categories[4]['leaders'], 'GAA')

def fetch_nhl_pim_leaders():
    categories = _fetch_nhl_data()
    if categories is None or len(categories) < 6:
        return pd.DataFrame()
    return _build_leaders_df(categories[5]['leaders'], 'PIM')