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
