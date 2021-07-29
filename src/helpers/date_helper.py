from datetime import datetime

def earliest_date(dates):
    filtered_dates = [date for date in dates if date is not None]
    filtered_dates.sort()
    return filtered_dates[0]

def latest_date(dates):
    filtered_dates = [date for date in dates if date is not None]
    filtered_dates.sort()
    return filtered_dates[-1]

def get_isoformat(date):
    if type(date) != datetime:
        return date
    else:
        return date.isoformat()