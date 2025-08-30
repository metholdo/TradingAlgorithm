
from __future__ import annotations
import pandas_market_calendars as mcal
from datetime import datetime, timezone

def is_market_open(dt: datetime | None = None) -> bool:
    dt = dt or datetime.now(timezone.utc)
    nyse = mcal.get_calendar("XNYS")
    schedule = nyse.schedule(start_date=dt.date(), end_date=dt.date())
    return mcal.date_range(schedule, frequency="1min").tz_convert(timezone.utc).between_time("14:30","21:00").size > 0
