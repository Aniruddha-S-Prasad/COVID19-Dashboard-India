# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:37:38 2020

@author: Aniruddha-S-Prasad
"""
import database_handler as dbhl
import plot_handler as plthl
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter

current_patient_database_filename = 'patients.db'
recovered_deaths_database_filename = 'recoveries_and_deaths.db'


class DataContainer:

    def __init__(self, beta: np.ndarray, gamma: np.ndarray, R_0: np.ndarray, offest_days: int, infected_count: np.ndarray, affected_count: np.ndarray, dates: list):
        self.beta = beta
        self.gamma = gamma
        self.R_0 = R_0
        self.offset_days = offest_days
        self.affected_count = affected_count
        self.infected_count = infected_count
        self.dates = dates


def generate_matrix(x: np.ndarray, j: int) -> np.ndarray:
    n = x.size - j + 1
    return np.array([x[i:i + j] for i in range(n-1)])


def predict_data(init_values: np.ndarray, coeff: np.ndarray, intercept: float, output_size: int) -> np.ndarray:
    order = coeff.size
    output = np.zeros(output_size)
    output[:len(init_values)] = init_values
    for index in range(output_size - order):
        output[index+order] = np.sum(np.multiply(coeff, output[index:index + order])) + intercept
    return output


def remove_outliers(array: np.ndarray, max_deviation: float) -> np.ndarray:
    for index in range(1,np.size(array)-1):
        tmp = array.copy()
        tmp[index] = np.nan
        tmp = interpolate_nans(tmp)
        if abs(array[index] - tmp[index]) > abs(array[index]*max_deviation):
            array[index] = np.nan
        tmp = []

    return array


def smooth_by_interpolation(array: np.ndarray) -> np.ndarray:
    for index in range(1, np.size(array)-1):
        array[index] = np.nan
        interpolate_nans(array)


def interpolate_nans(array: np.ndarray) -> np.ndarray:
    x = np.arange(np.size(array))
    array[np.isnan(array)]= np.interp(x[np.isnan(array)], x[~np.isnan(array)], array[~np.isnan(array)])
    return array


def exp_fit(x: np.ndarray, a: float, b: float) -> np.ndarray:
    return a * np.exp(b * x)


def lin_fit(x: np.ndarray, m: float, c: float) -> np.ndarray:
    return m * x + c


def main():

    from_date = date(2020, 3, 1)
    to_date = date.today() - timedelta(days=1)

    state = 'IN'
    database = dbhl.DatabaseHandler(from_date, to_date, state=state)

    dates = database.dates
    recovered_count = database.recovered_count
    deceased_count = database.deceased_count

    removed_count = recovered_count + deceased_count
    dremoved_count = removed_count - np.append(0, removed_count[:len(removed_count) - 1])

    affected_count = database.total_count

    infected_count = affected_count - removed_count
    dinfected_count = infected_count - np.append(0, infected_count[:len(infected_count) - 1])

    # population = 5 * np.max(affected_count)
    # susceptible_count = population - affected_count
    # dsusceptible_count = susceptible_count - np.append(0, susceptible_count[:len(susceptible_count)-1])

    offset_days = 21
    beta = np.divide(dinfected_count[offset_days:] + dremoved_count[offset_days:], infected_count[offset_days:])
    gamma = np.divide(dremoved_count[offset_days:], infected_count[offset_days:])
    gamma[gamma == 0] = np.nan
    beta[beta == 0] = np.nan
    # beta = remove_outliers(beta, 0.5)
    # gamma = remove_outliers(gamma, 0.5)
    smooth_by_interpolation(beta)
    smooth_by_interpolation(gamma)
    # beta = interpolate_nans(beta)
    # gamma = interpolate_nans(gamma)

    # TODO
    # order = 7
    # beta_matrix = generate_matrix(beta, order)
    # beta_fir = LinearRegression(n_jobs=-1).fit(beta_matrix, beta[order:])
    # beta_predict = predict_data(beta[:order], beta_fir.coef_, beta_fir.intercept_, np.size(beta)+30)
    
    # order = 5
    # gamma_matrix = generate_matrix(gamma, order)
    # gamma_fir = LinearRegression(n_jobs=-1).fit(gamma_matrix, gamma[order:])
    # gamma_predict = predict_data(gamma[:order], gamma_fir.coef_, gamma_fir.intercept_, np.size(gamma)+30)

    reproductive_number = np.divide(beta, gamma)
    # reproductive_number = remove_outliers(reproductive_number, 0.75)
    # #reproductive_number
    smooth_by_interpolation(reproductive_number)

    data = DataContainer(beta, gamma, reproductive_number, offset_days,  infected_count, affected_count, dates)

    plotter = plthl.PlotHandler()
    plotter.plot_all_data(data)

    # TODO
    # plotter.plot_data_and_fit(dates, offset_days, beta, beta_predict)
    # plotter.plot_data_and_fit(dates, offset_days, gamma, gamma_predict)

    # delta_days = 15
    # print(f'Exponential fit for data, using data until {dates[len(dates)-delta_days]}')
    # x = np.linspace(0, len(count)-delta_days, len(count)-delta_days)
    # param, param_cov = curve_fit(exp_fit, x, count[0:len(count)-delta_days], p0=[0.01, 1])
    #
    # x = np.linspace(0, len(count), len(count))
    #
    # plotter = plthl.PlotHandler()
    # plotter.plot_data_and_fit(dates, count, exp_fit(x, param[0], param[1]))

    plt.show()
    return 0


if __name__ == "__main__":
    main()
