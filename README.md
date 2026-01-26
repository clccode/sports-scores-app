# Sports Scores Dashboard

A real-time sports scores dashboard built with Streamlit, displaying live scores for NHL, NBA, and NFL games.

## Features

- 🏒 NHL scores and schedules
- 🏀 NBA scores and schedules
- 🏈 NFL scores and schedules
- 🕐 Timezone-aware game times
- 🎲 Pre-game odds (via DraftKings)
- 📊 Live game status with period/quarter info

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sports-scores-app.git
cd sports-scores-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

## Data Source

Scores and game data are fetched from ESPN's public API.

## Tech Stack

- Python 3.12+
- Streamlit
- Requests
- Pytz