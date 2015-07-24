#!/usr/bin/env python
from datetime import date, datetime

seasons = [('winter', (date(1,  1,  1),  date(1,  3, 20))),
           ('spring', (date(1,  3, 21),  date(1,  6, 20))),
           ('summer', (date(1,  6, 21),  date(1,  9, 22))),
           ('autumn', (date(1,  9, 23),  date(1, 12, 20))),
           ('winter', (date(1, 12, 21),  date(1, 12, 31)))]

def get_season(now):
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=1)
    for season, (start, end) in seasons:
        if start <= now <= end:
            return season
    assert 0, 'never happens'

