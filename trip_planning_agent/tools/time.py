import datetime
from zoneinfo import ZoneInfo


def get_current_time(timeZone: str) -> dict:
    """Returns the current time in a specified time zone.

    Args:
        timeZone (str): IANA time zone name (e.g. 'America/New_York').

    Returns:
        dict: status and result or error msg.
    """
    try:
        tz = ZoneInfo(timeZone)
        now = datetime.datetime.now(tz)
        report = f"The current time in {timeZone} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"
        return {"status": "success", "report": report}
    except Exception as e:
        return {"status": "error", "message": str(e)}
