"""ESPN API data fetching functions for various sports."""

import requests
from typing import Dict, List, Optional

def fetch_nhl_scores() -> Optional[Dict]:
    """Fetch current NHL scores and games."""
    url = "http://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching NHL scores: {e}")
        return None

def fetch_nba_scores() -> Optional[Dict]:
    """Fetch current NBA scores and games."""
    url = "http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching NBA scores: {e}")
        return None

def fetch_nfl_scores() -> Optional[Dict]:
    """Fetch current NFL scores and games."""
    url = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching NFL scores: {e}")
        return None

def fetch_premier_league_scores() -> Optional[Dict]:
    """Fetch current Premier League scores and games."""
    url = "http://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching Premier League scores: {e}")
        return None

def get_broadcast_info(game: Dict, sport: str = "nhl") -> str:
    """Extract all broadcast info from game data."""
    competition = game['competitions'][0]

    if 'broadcasts' not in competition or not competition['broadcasts']:
        return None

    broadcast_list = []

    for broadcast in competition['broadcasts']:
        channels = ", ".join(broadcast['names'])

        market = broadcast['market'].title()
        broadcast_list.append(f"{channels} ({market})")

    return " | ".join(broadcast_list) if broadcast_list else None

def parse_game_data(game: Dict, sport: str = "nhl") -> Dict:
    """
    Parse ESPN API game data into a normalized format.
    """
    status = game['status']
    competition = game['competitions'][0]

    # Get broadcast info
    broadcast = get_broadcast_info(game)

    # Safely get odds (may not exist for all games)
    odds = None
    if 'odds' in competition and len(competition['odds']) > 0 and competition['odds'][0] is not None:
        odds = competition['odds'][0].get('details', 'N/A')

    return {
        'state': status['type']['state'],
        'description': status['type']['description'],
        'period': status.get('period', 0),
        'game_status': status['type']['detail'],
        'clock': status.get('displayClock', '0:00'),
        'date': game['date'],
        'home_team': competition['competitors'][0]['team']['displayName'],
        'away_team': competition['competitors'][1]['team']['displayName'],
        'home_score': competition['competitors'][0]['score'],
        'away_score': competition['competitors'][1]['score'],
        'odds': odds,
        'broadcast': broadcast,
        'sport': sport
    }

def fetch_nhl_news() -> Optional[List[Dict]]:
    """Fetch latest NHL news articles."""
    try:
        url = "http://site.api.espn.com/apis/site/v2/sports/hockey/nhl/news"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        news_list = []
        for article in data['articles']:
            news_list.append({
                'headline': article['headline'],
                'url': article['links']['web']['href'],
                'description': article.get('description', ''),  # Some articles may not have this
                'published': article.get('published', '')
            })

        return news_list

    except Exception as e:
        print(f"Error fetching NHL news: {e}")
        return None

def fetch_nba_news() -> Optional[List[Dict]]:
    """Fetch latest NBA news articles."""
    try:
        url = "http://site.api.espn.com/apis/site/v2/sports/basketball/nba/news"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        news_list = []
        for article in data['articles']:
            news_list.append({
                'headline': article['headline'],
                'url': article['links']['web']['href'],
                'description': article.get('description', ''),
                'published': article.get('published', '')
            })

        return news_list

    except Exception as e:
        print(f"Error fetching NBA news: {e}")
        return None

def fetch_nfl_news() -> Optional[List[Dict]]:
    """Fetch latest NFL news articles."""
    try:
        url = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/news"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        news_list = []
        for article in data['articles']:
            news_list.append({
                'headline': article['headline'],
                'url': article['links']['web']['href'],
                'description': article.get('description', ''),
                'published': article.get('published', '')
            })

        return news_list

    except Exception as e:
        print(f"Error fetching NFL news: {e}")
        return None
    
def fetch_premier_league_news() -> Optional[List[Dict]]:
    """Fetch latest Premier League news articles."""
    try:
        url = "http://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/news"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        news_list = []
        for article in data['articles']:
            news_list.append({
                'headline': article['headline'],
                'url': article['links']['web']['href'],
                'description': article.get('description', ''),
                'published': article.get('published', '')
            })

        return news_list

    except Exception as e:
        print(f"Error fetching Premier League news: {e}")
        return None