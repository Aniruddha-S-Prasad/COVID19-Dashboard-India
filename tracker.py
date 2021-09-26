import json
import requests
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta

import plot_handler as plthl
import json_database_builder
from data_container import DataContainer


def smooth_by_interpolation(array: np.ndarray):
    for index in range(1, np.size(array)-1):
        array[index] = np.nan
        interpolate_nans(array)


def interpolate_nans(array: np.ndarray) -> np.ndarray:
    x = np.arange(np.size(array))
    array[np.isnan(array)] = np.interp(x[np.isnan(array)], x[~np.isnan(array)], array[~np.isnan(array)])
    return array


def delta_series(array: np.ndarray) -> np.ndarray:
    return array - np.append(0, array[:len(array)-1])


def change_factor_series(array: np.ndarray) -> np.ndarray:
    d_array = delta_series(array)
    return abs(np.divide(d_array, np.append(1, array[:len(array)-1])))


def data_analyser(state: str, smooth_data: bool) -> DataContainer:
    # from_date = date(2020, 3, 1)
    # to_date = date.today() - timedelta(days=1)
    # dates = []
    
    # month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # with open('databases/database.json', 'r') as db:
    #     database = json.load(db)

    # if database['to_date'] != f'{to_date.day:02d}-{month[to_date.month-1]}-{to_date.year}':
    #     json_database_builder.main()
    #     database = None
    #     with open('databases/database.json', 'r') as db:
    #         database = json.load(db)
    if state == 'IN':
        state = 'TT'
    
    api_url = 'https://data.covid19india.org/v4/min/timeseries.min.json'
    time_series_response = json.loads(requests.get(api_url).text)
    
    state_data = time_series_response[state]['dates']
    dates_str = list(state_data.keys())

    confirmed_daily = []
    deceased_daily = []
    recovered_daily = []
    dates = []

    for date_str in dates_str:
        dates.append(date.fromisoformat(date_str))
        try:
            confirmed_daily.append(int(state_data[date_str]['delta']['confirmed']))
        except KeyError:
            confirmed_daily.append(0)
        try:
            deceased_daily.append(int(state_data[date_str]['delta']['deceased']))
        except KeyError:
            deceased_daily.append(0)
        try:
            recovered_daily.append(int(state_data[date_str]['delta']['recovered']))
        except KeyError:
            recovered_daily.append(0)
    

    confirmed_daily = np.array(confirmed_daily)
    recovered_daily = np.array(recovered_daily)
    deceased_daily = np.array(deceased_daily)
        
    data_len = len(dates_str)

    total_count = np.cumsum(confirmed_daily)
    total_recovered = np.cumsum(recovered_daily)
    total_deceased = np.cumsum(deceased_daily)

    active_cases = total_count - total_recovered - total_deceased
    
    offset_days = 30

    # beta = np.divide(confirmed_daily[offset_days:], 1)
    beta = np.gradient(total_count[offset_days:])/active_cases[offset_days:]
    # beta = np.divide(confirmed_daily[offset_days:], active_cases[offset_days:])

    # gamma = np.divide(recovered_daily[offset_days:] + deceased_daily[offset_days:], 1)
    gamma = np.gradient(total_recovered[offset_days:] + total_deceased[offset_days:])/active_cases[offset_days:]
    # gamma = np.divide(recovered_daily[offset_days:] + deceased_daily[offset_days:], active_cases[offset_days:])

    if smooth_data:
        gamma[gamma == 0] = np.nan
        beta[beta == 0] = np.nan

        smooth_factor = 0.25
        beta[change_factor_series(beta) > smooth_factor] = np.nan
        smooth_by_interpolation(beta)

        smooth_factor = 0.80
        gamma[change_factor_series(gamma) > smooth_factor] = np.nan
        smooth_by_interpolation(gamma)

    reproductive_number = np.divide(beta, gamma)
    beta_len = len(beta)
    counts = np.zeros((5, data_len))
    counts[0, :] = total_count
    counts[1, :] = active_cases
    counts[2, :][:beta_len] = beta
    counts[3, :][:beta_len] = gamma
    counts[4, :][:beta_len] = reproductive_number

    return DataContainer(dates, offset_days, counts)
    

def main():
    from_date = date(2020, 3, 1)
    to_date = date.today() - timedelta(days=1)
    data = data_analyser('IN', False)
    
    plotter = plthl.PlotHandler()
    plotter.plot_all_data(data)
    print(f'As of {to_date}:')
    print(f'\tTotal Cases:\t{int(data.np_data[0, :][-1])}\n' +
          f'\tActive Cases:\t{int(data.np_data[1, :][-1])}\n' +
          f'\tPeak Cases:\t{int(max(data.np_data[1, :]))}')
    plt.show()


    return 0


if __name__ == "__main__":
    main()
