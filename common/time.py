from datetime import datetime

def get_next_week():
    current_time = datetime.now()
    #current_time = datetime(current_time.year, current_time.month, current_time.day + 7)
    weekday = current_time.weekday()
    current_day = current_time.day

    start_day = current_day - weekday
    end_date = current_day + (6 - weekday)

    start_time = datetime(current_time.year, current_time.month, start_day, 0,0,0)
    end_time = datetime(current_time.year, current_time.month, end_date, 23, 59, 59)


    return [start_time, end_time]
