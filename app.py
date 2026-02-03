"""Sports Scores Dashboard - Streamlit App"""

import streamlit as st
from streamlit_js import st_js
from espn_api import (fetch_nba_scores, fetch_nhl_scores, fetch_nfl_scores, fetch_premier_league_scores,
                      parse_game_data, fetch_nhl_news, fetch_nba_news, fetch_nfl_news, 
                      fetch_premier_league_news)
from nhl_stats import (fetch_nhl_points_leaders, fetch_nhl_goals_leaders, fetch_nhl_assists_leaders,
                       fetch_nhl_plus_minus_leaders, fetch_nhl_gaa_leaders, fetch_nhl_pim_leaders,
                       get_nhl_season_type)
from nba_stats import (fetch_nba_ppg_leaders, fetch_nba_assists_leaders, fetch_nba_fgp_leaders,
                       fetch_nba_rebounds_leaders, fetch_nba_ftp_leaders, fetch_nba_3pt_leaders,
                       fetch_nba_steals_leaders, get_nba_season_type)
from nfl_stats import (fetch_nfl_passing_leaders, fetch_nfl_rushing_leaders, fetch_nfl_receiving_leaders,
                       fetch_nfl_tackles_leaders, fetch_nfl_sacks_leaders, get_nfl_season_type)
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
        st.subheader("📊 NHL Statistics")
        st.caption(get_nhl_season_type())

        points_df = fetch_nhl_points_leaders()
        if not points_df.empty:
            st.subheader("Points Leaders")
            st.dataframe(points_df, width='stretch')
            st.divider()
        else:
            st.warning("Unable to load NHL Points leaders")

        goals_df = fetch_nhl_goals_leaders()
        if not goals_df.empty:
            st.subheader("Goals Leaders")
            st.dataframe(goals_df, width='stretch')
            st.divider()
        else:
            st.warning("Unable to load NHL Goals leaders")

        assists_df = fetch_nhl_assists_leaders()
        if not assists_df.empty:
            st.subheader("Assists Leaders")
            st.dataframe(assists_df, width='stretch')
            st.divider()
        else:
            st.warning("Unable to load NHL Assists leaders")

        plus_minus_df = fetch_nhl_plus_minus_leaders()
        if not plus_minus_df.empty:
            st.subheader("Plus/Minus Leaders")
            st.dataframe(plus_minus_df, width='stretch')
            st.divider()
        else:
            st.warning("Unable to load NHL Plus/Minus leaders")

        gaa_df = fetch_nhl_gaa_leaders()
        if not gaa_df.empty:
            st.subheader("Goals Against Average (GAA) Leaders")
            st.dataframe(gaa_df, width='stretch')
            st.divider()
        else:
            st.warning("Unable to load NHL GAA leaders")

        pim_df = fetch_nhl_pim_leaders()
        if not pim_df.empty:
            st.subheader("Penalty Minutes (PIM) Leaders")
            st.dataframe(pim_df, width='stretch')
        else:
            st.warning("Unable to load NHL PIM leaders")

    elif sport == "NBA":
        st.divider()
        st.subheader("📊 NBA Statistics")
        st.caption(get_nba_season_type())

        ppg_df = fetch_nba_ppg_leaders()
        if not ppg_df.empty:
            st.subheader("Points Per Game (PPG) Leaders")
            st.dataframe(ppg_df, width='stretch')
            st.divider()
        else:
            st.warning("Unable to load NBA PPG leaders")

        assists_df = fetch_nba_assists_leaders()
        if not assists_df.empty:
            st.subheader("Assists Per Game (APG) Leaders")
            st.dataframe(assists_df, width='stretch')
            st.divider()
        else:
            st.warning("Unable to load NBA APG leaders")

        fgp_df = fetch_nba_fgp_leaders()
        if not fgp_df.empty:
            st.subheader("Field Goal Percentage (FG%) Leaders")
            st.dataframe(fgp_df, width='stretch')
            st.divider()
        else:
            st.warning("Unable to load NBA FG% leaders")

        rebounds_df = fetch_nba_rebounds_leaders()
        if not rebounds_df.empty:
            st.subheader("Rebounds Per Game (RPG) Leaders")
            st.dataframe(rebounds_df, width='stretch')
            st.divider()
        else:
            st.warning("Unable to load NBA RPG leaders")

        ftp_df = fetch_nba_ftp_leaders()
        if not ftp_df.empty:
            st.subheader("Free Throw Percentage (FT%) Leaders")
            st.dataframe(ftp_df, width='stretch')
            st.divider()
        else:
            st.warning("Unable to load NBA FT% leaders")

        threept_df = fetch_nba_3pt_leaders()
        if not threept_df.empty:
            st.subheader("3-Point Percentage (3P%) Leaders")
            st.dataframe(threept_df, width='stretch')
            st.divider()
        else:
            st.warning("Unable to load NBA 3P% leaders")

        steals_df = fetch_nba_steals_leaders()
        if not steals_df.empty:
            st.subheader("Steals Per Game (SPG) Leaders")
            st.dataframe(steals_df, width='stretch')
        else:
            st.warning("Unable to load NBA SPG leaders")

    elif sport == "NFL":
        st.divider()
        st.subheader("📊 NFL Statistics")
        st.caption(get_nfl_season_type())

        passing_df = fetch_nfl_passing_leaders()
        if not passing_df.empty:
            st.subheader("Passing Yards Leaders")
            st.dataframe(passing_df, width='stretch')
            st.divider()
        else:
            st.warning("Unable to load NFL Passing leaders")

        rushing_df = fetch_nfl_rushing_leaders()
        if not rushing_df.empty:
            st.subheader("Rushing Yards Leaders")
            st.dataframe(rushing_df, width='stretch')
            st.divider()
        else:
            st.warning("Unable to load NFL Rushing leaders")

        receiving_df = fetch_nfl_receiving_leaders()
        if not receiving_df.empty:
            st.subheader("Receiving Yards Leaders")
            st.dataframe(receiving_df, width='stretch')
            st.divider()
        else:
            st.warning("Unable to load NFL Receiving leaders")

        tackles_df = fetch_nfl_tackles_leaders()
        if not tackles_df.empty:
            st.subheader("Total Tackles Leaders")
            st.dataframe(tackles_df, width='stretch')
            st.divider()
        else:
            st.warning("Unable to load NFL Tackles leaders")

        sacks_df = fetch_nfl_sacks_leaders()
        if not sacks_df.empty:
            st.subheader("Total Sacks Leaders")
            st.dataframe(sacks_df, width='stretch')
        else:
            st.warning("Unable to load NFL Sacks leaders")