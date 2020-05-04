import json
import requests
import csv
import numpy as np
import database_handler as dbhl
from typing import NamedTuple
from datetime import date, timedelta


def main():
    from_date = date(2020, 3, 1)
    to_date = date(2020, 3, 13)
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    with open('databases/state_codes.json') as state_codes:
        state_dict = json.load(state_codes)

    state_list = list(state_dict.keys())

    sql_db = dbhl.DatabaseHandler(from_date, to_date)

    api_url = 'https://api.covid19india.org/states_daily.json'
    # try:
    #     with open('databases/states_daily.json', 'r', encoding='utf-8') as daily_file:
    #         states_daily_json = json.load(daily_file)
    #         states_daily_list = states_daily_json['states_daily']
    # except FileNotFoundError:
    states_daily_response = requests.get(api_url)
    states_daily_json = json.loads(states_daily_response.text)
    states_daily_list = states_daily_json['states_daily']
    with open('databases/states_daily.json', 'w', encoding='utf-8') as daily_file:
        json.dump(states_daily_json, daily_file, ensure_ascii=False, indent=4)

    daily_confirmed = {}
    daily_recovered = {}
    daily_deceased = {}

    for state in state_list:
        # State counts from 1st March till 13th March
        _, confirmed_count = sql_db.get_total_count(state, cumulative=False)
        _, recovered_count = sql_db.get_recovered_count(state, cumulative=False)
        _, deceased_count = sql_db.get_deceased_count(state, cumulative=False)
        daily_confirmed[state] = confirmed_count.tolist()
        daily_recovered[state] = recovered_count.tolist()
        daily_deceased[state] = deceased_count.tolist()

    for item in states_daily_list:
        case = item['status']
        for state, count in item.items():
            if state == 'status' or state == 'date':
                continue
            state = state.upper()
            if count == '':
                count = 0
            count = int(count)
            if case == 'Confirmed':
                daily_confirmed[state].append(count)
            elif case == 'Recovered':
                daily_recovered[state].append(count)
            elif case == 'Deceased':
                daily_deceased[state].append(count)

    to_date = date.today() - timedelta(days=1)
    database = {}
    for state in state_list:
        data = {'Confirmed': daily_confirmed[state],
                'Recovered': daily_recovered[state],
                'Deceased': daily_deceased[state]}
        database[state] = data
    database['from_date'] = f'{from_date.day:02d}-{month[from_date.month-1]}-{from_date.year}'
    database['to_date'] = f'{to_date.day:02d}-{month[to_date.month-1]}-{to_date.year}'

    with open('databases/database.json', 'w', encoding='utf-8') as db:
        json.dump(database, db, ensure_ascii=False, indent=4)
    return


if __name__ == '__main__':
    main()
