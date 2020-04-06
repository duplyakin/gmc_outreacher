import datetime
from datetime import timedelta
from pprint import pprint

t_1 = {
    0 : False,
    1 : False,
    2 : False,
    3 : True,
    4 : False,
    5 : False,
    6 : False
}

def days_delta(a, current_day):
    delta = 1
    next_day = current_day + 1
    
    for i in range(6):
        if next_day > 6:
            next_day = 0

        if a.get(next_day):
            break

        delta = delta + 1
        next_day = next_day + 1

    return delta

current_day = 3
#print(days_delta(t_1, current_day))

next_action = datetime.datetime.now() + timedelta(days=1)
print(next_action)
next_action = next_action.replace(hour=10, minute=0)
print(next_action)