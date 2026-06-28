import requests
import pandas as pd

# Cache for API data to avoid multiple calls
_mlb_data_cache = None
_mlb_season_type = None

def _fetch_mlb_data():
    """Fetch MLB leaders data from ESPN API with error handling."""
    global _mlb_data_cache, _mlb_season_type

    if _mlb_data_cache is not None:
        return _mlb_data_cache

    url = "https://site.api.espn.com/apis/site/v3/sports/baseball/mlb/leaders"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        _mlb_data_cache = data['leaders']['categories']
        _mlb_season_type = data['currentSeason']['type']['name']
        return _mlb_data_cache
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Error fetching NBA data: {e}")
        return None

def get_mlb_season_type():
    """Get the current MLB season type (Regular Season, Postseason, etc.)."""
    if _mlb_season_type is not None:
        return _mlb_season_type

    # Fetch data to populate cache if not already done
    _fetch_mlb_data()
    return _mlb_season_type if _mlb_season_type else "Season"

def _build_leaders_df(leaders, stat_column_name, format_fn=None):
    """Helper function to build a DataFrame from leaders data."""
    if not leaders:
        return pd.DataFrame()

    try:
        # Calculate rank (make an exception for ERA where lower is better)
        # Use 'value' for numeric ranking — reliable float
        numeric_col = pd.Series([leader['value'] for leader in leaders], dtype=float)

        # Drop rows where value is missing
        valid_mask = numeric_col.notna()
        leaders_filtered = [l for l, v in zip(leaders, valid_mask) if v]
        numeric_col = numeric_col[valid_mask].reset_index(drop=True)

        df = pd.DataFrame({
            'Player': [l['athlete']['displayName'] for l in leaders_filtered],
            'Team': [l['team']['displayName'] for l in leaders_filtered],
            stat_column_name: [format_fn(l['value']) if format_fn else str(l['value']) for l in leaders_filtered]
        })

        if format_fn:
            df[stat_column_name] = [format_fn(leader['value']) for leader in leaders]
        else:
            df[stat_column_name] = [str(leader['value']) for leader in leaders]

        if stat_column_name == 'ERA':
            df['Rank'] = numeric_col.rank(method='min', ascending=True)
        else:
            df['Rank'] = numeric_col.rank(method='min', ascending=False)

        # sort by rank
        df = df.sort_values('Rank')

        #Create display rank with "T" for ties
        # Check if current rank appears more than once (is tied)
        rank_counts = df['Rank'].value_counts()
        df['Display_Rank'] = df['Rank'].apply(
            lambda rank: f"T{int(rank)}" if rank_counts[rank] > 1 else str(int(rank))
            )
        # Set Display_Rank as index
        df = df.set_index('Display_Rank')
        df.index.name = 'Rank'

        # Drop the numeric Rank column
        df = df.drop('Rank', axis=1)
        return df
    except (KeyError, TypeError, ValueError) as e:
        print(f"Error building DataFrame: {e}")
        return pd.DataFrame()
    
# individual stats data frames
def fetch_mlb_batting_avg_leaders():
    categories = _fetch_mlb_data()
    if categories is None or len(categories) < 1:
        return pd.DataFrame()
    return _build_leaders_df(
        categories[0]['leaders'],
        'AVG',
        format_fn=lambda v: f"{v:.3f}".lstrip('0')  # 0.336 → .336
    )

def fetch_mlb_home_runs_leaders():
    categories = _fetch_mlb_data()
    if categories is None or len(categories) < 2:
        return pd.DataFrame()
    return _build_leaders_df(
        categories[1]['leaders'],
        'HR',
        format_fn=lambda v: str(int(v))  # Ensure HR is displayed as an integer
    )

def fetch_mlb_rbi_leaders():
    categories = _fetch_mlb_data()
    if categories is None or len(categories) < 3:
        return pd.DataFrame()
    return _build_leaders_df(
        categories[2]['leaders'],
        'RBI',
        format_fn=lambda v: str(int(v))  # Ensure RBI is displayed as an integer
    )

def fetch_mlb_era_leaders():
    categories = _fetch_mlb_data()
    if categories is None or len(categories) < 4:
        return pd.DataFrame()
    return _build_leaders_df(
        categories[7]['leaders'],
        'ERA',
        format_fn=lambda v: f"{v:.2f}"  # Format ERA to two decimal places
    )