import ast, json
import datetime as dt
import random

with open('resources/hour_weights.json') as fin:
    hour_weights = json.load(fin)
with open('resources/week_day_weights.json') as fin:
    week_day_weights = json.load(fin)
    week_day_weights = {ast.literal_eval(k): v for k, v in week_day_weights.items()}

def get_weighted_timestamps(date, max_trans_per_daty):
    timestamps = []
    weight = week_day_weights[(date.weekday(), date.day//7+1)]
    num_transactions = int(max_trans_per_daty*weight)
    
    for _ in range(num_transactions):
        # Randomly select an hour with the given weightage
        hour = random.choices(range(24), hour_weights.values())[0]

        # Randomly generate minutes and seconds
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        # Create a timestamp
        timestamp = dt.datetime(year=date.year, month=date.month, day=date.day, hour=hour, minute=minute, second=second)
        
        timestamps.append(timestamp)
    
    return sorted(timestamps)

def generate_fake_dates(start_date, end_date, max_trans_per_daty):
    assert(isinstance(start_date, dt.date))
    assert(isinstance(end_date, dt.date))
    assert(start_date<end_date)

    curr_date = start_date
    timestamps = []
    while curr_date <= end_date:
        print('curr_date:', curr_date, end='\r')
        timestamps += get_weighted_timestamps(curr_date, max_trans_per_daty)
        curr_date += dt.timedelta(days=1)
    print('\n')
    return timestamps

if __name__=='__main__':
    start_date = dt.date(2021,1,1)
    end_date = dt.date(2023, 11, 1)
    timestamps = generate_fake_dates(start_date, end_date, 500)
    print('Writing result to file')
    with open('results.txt', 'w') as fout:
        for ts in timestamps:
            fout.write(ts.strftime('%Y-%m-%d %H:%M:%S\n'))
