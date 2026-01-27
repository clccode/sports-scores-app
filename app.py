"""Sports Scores Dashboard - Streamlit App"""

import streamlit as st
from espn_api import (fetch_nba_scores, fetch_nhl_scores, fetch_nfl_scores, parse_game_data,
                      fetch_nhl_news, fetch_nba_news, fetch_nfl_news)
from formatters import format_game_time

# Page config
st.set_page_config(page_title="Sports Scores", page_icon="🏒", layout="wide")

# Sidebar
st.sidebar.header("Settings")
sport = st.sidebar.selectbox("Sport", ["NHL", "NBA", "NFL"])
timezone = st.sidebar.selectbox(
    "Timezone",
    ["America/New_York", "America/Chicago", "America/Denver","America/Los_Angeles"]
)

if st.sidebar.button("🔄 Refresh"):
    st.rerun()  # Forces the whole app to re-run, fetching fresh data

st.title(f"{sport}")

raw_data = None
sport_code = ""
sport_icon = ""

if sport == "NHL":
    raw_data = fetch_nhl_scores()
    sport_code = "nhl"
    sport_icon = "🏒"
elif sport == "NBA":
    raw_data = fetch_nba_scores()
    sport_code = "nba"
    sport_icon = "🏀"
elif sport == "NFL":
    raw_data = fetch_nfl_scores()
    sport_code = "nfl"
    sport_icon = "🏈"

if raw_data:
    st.subheader(f"{sport_icon} {sport} Scores")
    for game in raw_data.get('events', []):
        game_data = parse_game_data(game, sport_code)

        if game_data['state'] == 'pre':
            game_time = format_game_time(game_data['date'], timezone)
            st.info(f"{game_data['away_team']} @ {game_data['home_team']} - {game_time}\n\n"
                        f"Odds: {game_data['odds']}\n")

        elif game_data['state'] == 'in':
            st.success(f"{game_data['away_team']} {game_data['away_score']} @ "
                       f"{game_data['home_team']} {game_data['home_score']}\n\n"
                       f"{game_data['game_status']}")

        else:
            st.write(f"{game_data['away_team']} {game_data['away_score']} @ "
                     f"{game_data['home_team']} {game_data['home_score']} - {game_data['game_status']}")

    # News section
    st.divider()
    st.subheader(f"📰 {sport} News")

    # Fetch news based on sport
    if sport == "NHL":
        news = fetch_nhl_news()
    elif sport == "NBA":
        news = fetch_nba_news()
    elif sport == "NFL":
        news = fetch_nfl_news()

    if news:
        for i, article in enumerate(news[:5], 1):  # Show top 5 articles
            with st.expander(f"{i}. {article['headline']}", expanded=(i == 1)):
                if article['description']:
                    st.write(article['description'])
                st.markdown(f"[Read full article]({article['url']})")
    else:
        st.warning(f"Unable to load {sport} news")