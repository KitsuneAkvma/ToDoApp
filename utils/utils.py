import datetime


def get_time(*date):
    if date:
        time_now = datetime.datetime.now()
        formatted_time_now = time_now.strftime("%c")
        return formatted_time_now
    else:
        formatted_time = datetime.datetime(date).strftime("%c")
        return formatted_time
