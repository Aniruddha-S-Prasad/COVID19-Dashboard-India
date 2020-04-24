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

    from_date = date(2020, 3, 1)
    to_date = date.today() - timedelta(days=1)

    state = 'IN'
    database = dbhl.DatabaseHandler(from_date, to_date, state=state)

    dates = database.dates
    recovered_count = database.recovered_count
    deceased_count = database.deceased_count

    removed_count = recovered_count + deceased_count
    dremoved_count = delta_series(removed_count)

    affected_count = database.total_count

    infected_count = affected_count - removed_count
    dinfected_count = delta_series(infected_count)

    offset_days = 21
    beta = np.divide(dinfected_count[offset_days:] + dremoved_count[offset_days:], infected_count[offset_days:])
    gamma = np.divide(dremoved_count[offset_days:], infected_count[offset_days:])
    gamma[gamma == 0] = np.nan
    beta[beta == 0] = np.nan
    smooth_factor = 0.25
    beta[change_factor_series(beta) > smooth_factor] = np.nan
    smooth_by_interpolation(beta)

    smooth_factor = 0.80
    gamma[change_factor_series(gamma) > smooth_factor] = np.nan
    smooth_by_interpolation(gamma)

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
    # smooth_by_interpolation(reproductive_number)

    data = DataContainer(beta, gamma, reproductive_number, offset_days,  infected_count, affected_count, dates)

    plotter = plthl.PlotHandler()
    plotter.plot_all_data(data)

    plt.show()
    return 0


if __name__ == "__main__":
    main()
