import json
import json_database_builder
import plot_handler as plthl
import numpy as np
import matplotlib.pyplot as plt
from tracker import DataContainer
from datetime import date, timedelta


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
    recovered_daily = np.array(state_data['Recovered'])
    deceased_daily = np.array(state_data['Deceased'])
    confirmed_daily = np.array(state_data['Confirmed'])

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
    beta = np.divide(confirmed_daily[offset_days:], active_cases[offset_days:])
    gamma = np.divide(recovered_daily[offset_days:] + deceased_daily[offset_days:], active_cases[offset_days:])

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

    data = DataContainer(beta, gamma, reproductive_number, offset_days,  active_cases, total_count, dates)

    plotter = plthl.PlotHandler()
    plotter.plot_all_data(data)

    plt.show()
    return 0


if __name__ == "__main__":
    main()
