"""Sports Scores Dashboard - Streamlit App"""

import streamlit as st
from streamlit_js import st_js
from espn_api import (fetch_nba_scores, fetch_nhl_scores, fetch_nfl_scores, fetch_premier_league_scores,
                      parse_game_data, fetch_nhl_news, fetch_nba_news, fetch_nfl_news, 
                      fetch_premier_league_news)
from nhl_stats import (fetch_nhl_points_leaders, fetch_nhl_goals_leaders, fetch_nhl_assists_leaders, 
                       fetch_nhl_plus_minus_leaders, fetch_nhl_gaa_leaders, fetch_nhl_pim_leaders)
from nba_stats import (fetch_nba_ppg_leaders, fetch_nba_assists_leaders, fetch_nba_fgp_leaders, 
                       fetch_nba_rebounds_leaders, fetch_nba_ftp_leaders, fetch_nba_3pt_leaders, 
                       fetch_nba_steals_leaders)
from nfl_stats import (fetch_nfl_passing_leaders, fetch_nfl_rushing_leaders, fetch_nfl_receiving_leaders, 
                       fetch_nfl_tackles_leaders, fetch_nfl_sacks_leaders)
from formatters import format_game_time
import pytz

# Page config
st.set_page_config(page_title="Sports Scores", page_icon="🏅", layout="wide")

# Sidebar
st.sidebar.header("Settings")
sport = st.sidebar.selectbox("Sport", ["NHL", "NBA", "NFL", "Premier League"])

# Get the user's timezone using JavaScript's Intl API
user_tz = st_js("""
  try {
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
  } catch (e) {
    return null;
  }
""",
    key="user-timezone",
)

# Timezone selection with default to user's timezone
default_timezone = user_tz[0] if user_tz else "America/New_York"

timezone_options = pytz.common_timezones
              
if default_timezone in timezone_options:                                                                                                            
      default_index = timezone_options.index(default_timezone)                                                                                        
else:                                                                                                                                               
    default_index = 0                                                                                                                               
                                                                                                                                                      
selected_tz = st.sidebar.selectbox("Timezone", timezone_options, index=default_index)

st.sidebar.caption(f"Detected Timezone: {default_timezone}")

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
elif sport == "Premier League":
    raw_data = fetch_premier_league_scores()
    sport_code = "eng.1"
    sport_icon = "⚽"

if raw_data:
    st.subheader(f"{sport_icon} {sport} Scores")
    for game in raw_data.get('events', []):
        game_data = parse_game_data(game, sport_code)

        if game_data['state'] == 'pre':
            game_time = format_game_time(game_data['date'], selected_tz)
            broadcast_text = f"\n\nWatch: {game_data['broadcast']}" if game_data.get('broadcast') else ""
            if sport_code != 'eng.1':
                st.info(f"{game_data['away_team']} @ {game_data['home_team']} - {game_time}\n\n"
                        f"Odds: {game_data['odds']}\n\n{broadcast_text}")
            else:
                st.info(f"{game_data['home_team']} vs {game_data['away_team']} - {game_time}\n\n{broadcast_text}")

        elif game_data['state'] == 'in':
            broadcast_text = f"\n\nWatch: {game_data['broadcast']}" if game_data.get('broadcast') else ""
            if sport_code != 'eng.1':
                st.success(f"{game_data['away_team']} {game_data['away_score']} @ "
                    f"{game_data['home_team']} {game_data['home_score']}\n\n"
                    f"{game_data['game_status']}\n\n{broadcast_text}")
            else:
                st.success(f"{game_data['home_team']} {game_data['home_score']} vs "
                    f"{game_data['away_score']} {game_data['away_team']}\n\n"
                    f"{game_data['game_status']}\n\n{broadcast_text}")

        else:
            if sport_code != 'eng.1':
                st.write(f"{game_data['away_team']} {game_data['away_score']} @ "
                     f"{game_data['home_team']} {game_data['home_score']} - {game_data['game_status']}")
            else:
                st.write(f"{game_data['home_team']} {game_data['home_score']} - "
                         f"{game_data['away_score']} {game_data['away_team']} - {game_data['game_status']}")

    # News section
    st.divider()
    st.subheader(f"📰 {sport} News")
    st.caption("News from ESPN")

    # Fetch news based on sport
    if sport == "NHL":
        news = fetch_nhl_news()
    elif sport == "NBA":
        news = fetch_nba_news()
    elif sport == "NFL":
        news = fetch_nfl_news()
    elif sport == "Premier League":
        news = fetch_premier_league_news()

    if news:
        for i, article in enumerate(news[:5], 1):  # Show top 5 articles
            with st.expander(f"{i}. {article['headline']}", expanded=(i == 1)):
                if article['description']:
                    st.write(article['description'])
                st.markdown(f"[Read full article]({article['url']})")
    else:
        st.warning(f"Unable to load {sport} news")

    # Stats Section
    if sport == "NHL":
        st.divider()
        st.subheader("NHL Points Leaders")
        points_df = fetch_nhl_points_leaders()
        st.dataframe(points_df, width='stretch')
        st.divider()

        goals_df = fetch_nhl_goals_leaders()
        st.subheader("NHL Goals Leaders")
        st.dataframe(goals_df, width='stretch')
        st.divider()

        assists_df = fetch_nhl_assists_leaders()
        st.subheader("NHL Assists Leaders")
        st.dataframe(assists_df, width='stretch')
        st.divider()

        plus_minus_df = fetch_nhl_plus_minus_leaders()
        st.subheader("NHL Plus/Minus Leaders")
        st.dataframe(plus_minus_df, width='stretch')
        st.divider()

        gaa_df = fetch_nhl_gaa_leaders()
        st.subheader("NHL Goals Against Average (GAA) Leaders")
        st.dataframe(gaa_df, width='stretch')
        st.divider()

        pim_df = fetch_nhl_pim_leaders()
        st.subheader("NHL Penalty Minutes (PIM) Leaders")
        st.dataframe(pim_df, width='stretch')

    elif sport == "NBA":
        st.divider()
        st.subheader("NBA Points Per Game (PPG) Leaders")
        ppg_df = fetch_nba_ppg_leaders()
        st.dataframe(ppg_df, width='stretch')
        st.divider()

        st.subheader("NBA Assists Per Game (APG) Leaders")
        assists_df = fetch_nba_assists_leaders()
        st.dataframe(assists_df, width='stretch')
        st.divider()

        st.subheader("NBA Field Goal Percentage (FG%) Leaders")
        fgp_df = fetch_nba_fgp_leaders()
        st.dataframe(fgp_df, width='stretch')
        st.divider()

        st.subheader("NBA Rebounds Per Game (RPG) Leaders")
        rebounds_df = fetch_nba_rebounds_leaders()
        st.dataframe(rebounds_df, width='stretch')
        st.divider()

        st.subheader("NBA Free Throw Percentage (FT%) Leaders")
        ftp_df = fetch_nba_ftp_leaders()
        st.dataframe(ftp_df, width='stretch')
        st.divider()

        st.subheader("NBA 3-Point Percentage (3P%) Leaders")
        threept_df = fetch_nba_3pt_leaders()
        st.dataframe(threept_df, width='stretch')
        st.divider()

        st.subheader("NBA Steals Per Game (SPG) Leaders")
        steals_df = fetch_nba_steals_leaders()
        st.dataframe(steals_df, width='stretch')

    elif sport == "NFL":
        st.divider()
        st.subheader("NFL Passing Yards Leaders")
        passing_df = fetch_nfl_passing_leaders()
        st.dataframe(passing_df, width='stretch')

        st.divider()
        st.subheader("NFL Rushing Yards Leaders")
        rushing_df = fetch_nfl_rushing_leaders()
        st.dataframe(rushing_df, width='stretch')

        st.divider()
        st.subheader("NFL Receiving Yards Leaders")
        receiving_df = fetch_nfl_receiving_leaders()
        st.dataframe(receiving_df, width='stretch')

        st.divider()
        st.subheader("NFL Total Tackles Leaders")
        tackles_df = fetch_nfl_tackles_leaders()
        st.dataframe(tackles_df, width='stretch')

        st.divider()
        st.subheader("NFL Total Sacks Leaders")
        sacks_df = fetch_nfl_sacks_leaders()
        st.dataframe(sacks_df, width='stretch')