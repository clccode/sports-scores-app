import requests
import pandas as pd

# Cache for API data to avoid multiple calls
_nfl_data_cache = None
_nfl_season_type = None

def _fetch_nfl_data():
    """Fetch NFL leaders data from ESPN API with error handling."""
    global _nfl_data_cache, _nfl_season_type

    if _nfl_data_cache is not None:
        return _nfl_data_cache

    url = "https://site.api.espn.com/apis/site/v3/sports/football/nfl/leaders"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        _nfl_data_cache = data['leaders']['categories']
        _nfl_season_type = data['currentSeason']['type']['name']
        return _nfl_data_cache
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Error fetching NFL data: {e}")
        return None

def get_nfl_season_type():
    """Get the current NFL season type (Regular Season, Postseason, etc.)."""
    if _nfl_season_type is not None:
        return _nfl_season_type

    # Fetch data to populate cache if not already done
    _fetch_nfl_data()
    return _nfl_season_type if _nfl_season_type else "Season"

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

def fetch_nfl_passing_leaders():
    categories = _fetch_nfl_data()
    if categories is None or len(categories) < 1:
        return pd.DataFrame()
    return _build_leaders_df(categories[0]['leaders'], 'Yards')

def fetch_nfl_rushing_leaders():
    categories = _fetch_nfl_data()
    if categories is None or len(categories) < 2:
        return pd.DataFrame()
    return _build_leaders_df(categories[1]['leaders'], 'Yards')

def fetch_nfl_receiving_leaders():
    categories = _fetch_nfl_data()
    if categories is None or len(categories) < 3:
        return pd.DataFrame()
    return _build_leaders_df(categories[2]['leaders'], 'Yards')

def fetch_nfl_tackles_leaders():
    categories = _fetch_nfl_data()
    if categories is None or len(categories) < 4:
        return pd.DataFrame()
    return _build_leaders_df(categories[3]['leaders'], 'Tackles')

def fetch_nfl_sacks_leaders():
    categories = _fetch_nfl_data()
    if categories is None or len(categories) < 5:
        return pd.DataFrame()
    return _build_leaders_df(categories[4]['leaders'], 'Sacks')