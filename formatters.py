"""Utility functions for formatting times and game data."""

from datetime import datetime
import pytz


def format_game_time(utc_time_string: str, timezone: str = "America/New_York") -> str:
    """
    Convert UTC game time to user's local timezone.

    Args:
        utc_time_string: ISO format UTC time from ESPN API
        timezone: Timezone string (e.g., 'America/New_York')

    Returns:
        Formatted time string like "3:00 PM"
    """
    user_tz = pytz.timezone(timezone)
    game_time_utc = datetime.fromisoformat(utc_time_string.replace('Z', '+00:00'))
    game_time_local = game_time_utc.astimezone(user_tz)

    # Platform-safe formatting
    hour = game_time_local.hour
    minute = game_time_local.minute
    am_pm = "AM" if hour < 12 else "PM"
    display_hour = hour if hour <= 12 else hour - 12
    display_hour = 12 if display_hour == 0 else display_hour

    return f"{display_hour}:{minute:02d} {am_pm}"