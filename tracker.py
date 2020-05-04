import json
import json_database_builder
import plot_handler as plthl
import numpy as np
import matplotlib.pyplot as plt
from typing import NamedTuple
from datetime import date, timedelta


class DataContainer(NamedTuple):
    dates: list
    offset_days: int
    np_data: np.ndarray
    members = {'total_count': 0,
               'active_cases': 1,
               'beta': 2,
               'gamma': 3,
               'reproductive_number': 4}


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


def get_gamma():
    return


def main():

    state = 'IN'
    smooth_data = False

    from_date = date(2020, 3, 1)
    to_date = date.today() - timedelta(days=1)
    dates = []
    
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    with open('databases/database.json', 'r') as db:
        database = json.load(db)

    if database['to_date'] != f'{to_date.day:02d}-{month[to_date.month-1]}-{to_date.year}':
        json_database_builder.main()
        database = None
        with open('databases/database.json', 'r') as db:
            database = json.load(db)

    if state == 'IN':
        state = 'TT'
    state_data = database[state]
    
    data_len = len(state_data['Confirmed'])
    recovered_daily = np.array(state_data['Recovered'], dtype=int)
    deceased_daily = np.array(state_data['Deceased'], dtype=int)
    confirmed_daily = np.array(state_data['Confirmed'], dtype=int)

    total_count = np.zeros(data_len)
    total_recovered = np.zeros(data_len)
    total_deceased = np.zeros(data_len)
    for index in range(data_len):
        dates.append(from_date + timedelta(days=index))

        total_count[index] = np.sum(confirmed_daily[:index+1])
        total_recovered[index] = np.sum(recovered_daily[:index+1])
        total_deceased[index] = np.sum(deceased_daily[:index+1])
    active_cases = total_count - total_recovered - total_deceased
    
    offset_days = 21

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

    data = DataContainer(dates, offset_days, counts)
    
    plotter = plthl.PlotHandler()
    plotter.plot_all_data(data)
    print(f'As of {to_date}:')
    print(f'\tTotal Cases:\t{int(total_count[-1])}\n' +
          f'\tActive Cases:\t{int(active_cases[-1])}\n' +
          f'\tPeak Cases:\t{int(max(active_cases))}')
    plt.show()


    return 0


if __name__ == "__main__":
    main()
