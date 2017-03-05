from datetime import datetime, date


def parse_date(date_string):
    try:
        event_date = datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        event_date = datetime.strptime(date_string, '%Y_%m_%d')
    return event_date.date()


def parse_datetime(dt_string):
    try:
        event_date = datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        event_date = datetime.strptime(dt_string, '%Y_%m_%d %H:%M:%S')
    return event_date