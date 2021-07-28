from datetime import datetime

def get_isoformat(date):
    if type(date) != datetime:
        return date
    else:
        return date.isoformat()