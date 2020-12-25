from datetime import datetime

def reverse_venue(venue):
    return 'home' if venue == 'away' else 'away'

def get_season_from_date(datestring):
    date = datetime.strptime(datestring, '%Y-%m-%d')

    threshold = 9 if date.year == 2020 else 8

    if date.month >= threshold:
        return f'{str(date.year)}-{str(date.year+1)[2:4]}'
    else:
        return f'{str(date.year-1)}-{str(date.year)[2:4]}'