import requests
import pandas as pd

# Cache for API data to avoid multiple calls
_nhl_data_cache = None

def _fetch_nhl_data():
    """Fetch NHL leaders data from ESPN API with error handling."""
    global _nhl_data_cache

    if _nhl_data_cache is not None:
        return _nhl_data_cache

    url = "https://site.api.espn.com/apis/site/v3/sports/hockey/nhl/leaders"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        _nhl_data_cache = data['leaders']['categories']
        return _nhl_data_cache
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Error fetching NHL data: {e}")
        return None

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
        df.index = range(1, len(df) + 1)
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