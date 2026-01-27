"""Sports Scores Dashboard - Streamlit App"""

import streamlit as st
from espn_api import fetch_nba_scores, fetch_nhl_scores, fetch_nfl_scores,parse_game_data
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

st.title("Sports Scores")

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
    st.subheader(f"{sport} {sport_icon}")
    for game in raw_data.get('events', []):
        game_data = parse_game_data(game, sport_code)

        if game_data['state'] == 'pre':
            game_time = format_game_time(game_data['date'], timezone)
            if sport == "NHL":
                st.info(f"{game_data['away_team']} @ {game_data['home_team']} - {game_time}\n\n"
                        f"Odds: {game_data['odds']}\n")
            elif sport == "NBA":
                st.info(f"{game_data['away_team']} @ {game_data['home_team']} - {game_time}\n\n"
                        f"Spread: {game_data['odds']}\n")

        elif game_data['state'] == 'in':
            st.success(f"{game_data['away_team']} {game_data['away_score']} @ "
                       f"{game_data['home_team']} {game_data['home_score']}\n\n"
                       f"{game_data['game_status']}")

        else:
            st.write(f"{game_data['away_team']} {game_data['away_score']} @ "
                     f"{game_data['home_team']} {game_data['home_score']} - {game_data['game_status']}")