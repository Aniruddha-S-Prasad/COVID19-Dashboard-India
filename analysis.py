from sklearn.linear_model import LinearRegression
import database_handler
import plot_handler
import numpy as np
from scipy.stats import linregress as lin_reg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date, timedelta


def delta_series(array: np.ndarray) -> np.ndarray:
    return array - np.append(0, array[:len(array)-1])


def change_factor_series(array: np.ndarray) -> np.ndarray:
    d_array = delta_series(array)
    return abs(np.divide(d_array, np.append(1, array[:len(array)-1])))


def interpolate_nans(array: np.ndarray):
    x = np.arange(np.size(array))
    array[np.isnan(array)] = np.interp(x[np.isnan(array)], x[~np.isnan(array)], array[~np.isnan(array)])


def smooth_by_interpolation(array: np.ndarray):
    for index in range(1, np.size(array)-1):
        array[index] = np.nan
        interpolate_nans(array)


def generate_matrix(x: np.ndarray, j: int) -> np.ndarray:
    n = x.size - j + 1
    return np.array([x[i:i + j] for i in range(n-1)])


def predict_data(init_values: np.ndarray, fir_model: LinearRegression, output_size: int) -> np.ndarray:
    if len(init_values) != len(fir_model.coef_):
        raise ValueError
    order = len(fir_model.coef_)
    output = np.zeros(output_size)
    output[:order] = init_values
    for index in range(output_size - order):
        output[index+order] = np.sum(np.multiply(fir_model.coef_, output[index:index + order])) + fir_model.intercept_
    return output


def predict_infected_count(beta: np.ndarray, gamma: np.ndarray, infected_count: np.ndarray,
                           offset_days: int, output_size: int) -> np.ndarray:

    output = np.zeros(output_size)
    output[0] = infected_count[offset_days]
    for index in range(1, output_size):
        output[index] = (1 + beta[index-1] - gamma[index - 1])*output[index-1]
    return output


def main():
    from_date = date(2020, 3, 1)
    to_date = date.today() - timedelta(days=1)

    state = 'KA'
    database = database_handler.DatabaseHandler(from_date, to_date, state=state)

    dates = database.dates

    recovered_count = database.recovered_count
    deceased_count = database.deceased_count
    removed_count = recovered_count + deceased_count
    dremoved_count = delta_series(removed_count)

    affected_count = database.total_count

    infected_count = affected_count - removed_count
    dinfected_count = delta_series(infected_count)

    offset_days = 21
    beta = (dinfected_count[offset_days:] + dremoved_count[offset_days:]) / infected_count[offset_days:]
    gamma = dremoved_count[offset_days:]/infected_count[offset_days:]
    dates_beta = dates[offset_days:]
    dates_gamma = dates[offset_days:]

    smooth_factor = 0.25
    beta[change_factor_series(beta) > smooth_factor] = np.nan
    smooth_by_interpolation(beta)

    smooth_factor = 0.80
    gamma[change_factor_series(gamma) > smooth_factor] = np.nan
    smooth_by_interpolation(gamma)

    x = np.arange(np.size(gamma))
    slope, intercept, _, _, _ = lin_reg(x, gamma)
    r_0 = beta/gamma

    order = 14
    beta_matrix = generate_matrix(beta, order)
    beta_fir = LinearRegression(n_jobs=-1).fit(beta_matrix, beta[order:])

    predict_offset = 15
    num_predictions = 10
    beta_predict = predict_data(beta[predict_offset:order + predict_offset], beta_fir, order + num_predictions)
    dates_predict = [dates_beta[predict_offset]]
    for index in range(1, len(beta_predict)):
        dates_predict.append(dates_predict[index - 1] + timedelta(days=1))

    x_predict = np.arange(order + num_predictions)
    x_predict = x_predict + predict_offset
    gamma_predict = slope*x_predict + intercept

    r_0_predict = beta_predict/gamma_predict

    fig, ax = plt.subplots()
    ax.plot(dates, infected_count, '-o')
    ax.plot(dates_predict, predict_infected_count(beta_predict, gamma_predict, infected_count, predict_offset+offset_days, order+num_predictions), '-x')
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    ax.format_xdata = mdates.DateFormatter('%d/%m/%Y')
    fig.autofmt_xdate()
    ax.grid(True)

    plt.show()
    return 0


if __name__ == '__main__':
    main()
    print('Cannot run file!!!')
