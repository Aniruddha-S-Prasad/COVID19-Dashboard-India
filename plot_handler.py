# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:39:10 2020

@author: Aniruddha-S-Prasad
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta
from data_container import DataContainer


class PlotHandler:

    def plot_all_data(self, data: DataContainer):
        x_axis = mdates.date2num(data.dates)

        raw_count_fig, raw_count_ax = plt.subplots(2, 1)
        raw_count_fig.suptitle('Counts')
        raw_count_ax[0].plot(x_axis, data.np_data[data.members['total_count'], :], '-o', color='tab:orange')
        raw_count_ax[0].set_title('Affected People')
        raw_count_ax[1].plot(x_axis, data.np_data[data.members['active_cases'], :], '-o', color='tab:red')
        raw_count_ax[1].set_title('Active Cases')

        for ax in raw_count_ax.flat:
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
            ax.format_xdata = mdates.DateFormatter('%d/%m/%Y')
            ax.set_xlabel('Time')
            ax.set_ylabel('Count')
            ax.label_outer()
            ax.grid(True)

        raw_count_fig.autofmt_xdate()

        analysis_fig, analysis_ax = plt.subplots(3, sharex=True)
        analysis_fig.suptitle('Analysed Data')
        date_len = len(x_axis[data.offset_days:])
        analysis_ax[0].plot(x_axis[data.offset_days:], data.np_data[data.members['gamma'], :][:date_len], '-o', color='tab:green')
        analysis_ax[0].set_title('Gamma')
        analysis_ax[1].plot(x_axis[data.offset_days:], data.np_data[data.members['beta'], :][:date_len], '-o', color='xkcd:goldenrod')
        analysis_ax[1].set_title('Beta')

        x_axis = []
        x_axis[:len(data.dates[data.offset_days:])] = data.dates[data.offset_days:]
        for i in range(len(data.dates[data.offset_days:]), date_len):
            x_axis.append(x_axis[i - 1] + timedelta(days=1))

        x_axis = mdates.date2num(x_axis)
        analysis_ax[2].plot(x_axis, data.np_data[data.members['reproductive_number'], :][:date_len], '-o', color='purple')
        analysis_ax[2].set_title('Reproductive number')

        for ax in analysis_ax.flat:
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
            ax.format_xdata = mdates.DateFormatter('%d/%m/%Y')
            ax.set_xlabel('Time')
            # ax.label_outer()
            ax.grid(True)

        analysis_fig.autofmt_xdate()

        return

    def plot_data(self, x: np.ndarray, y: np.ndarray, label: str, show_data=False, threshold=100) -> None:

        x_axis = mdates.date2num(x)
        fig, ax = plt.subplots()

        ax.plot(x_axis, y, '-o')

        ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        ax.format_xdata = mdates.DateFormatter('%d-%m-%Y')

        ax.set_xlabel('Dates')
        ax.set_ylabel(label)
        fig.autofmt_xdate()

        if show_data:
            y_max = y.max()
            for i in range(0, len(y), 1):
                if y[i] > threshold:
                    xy = (x[i] + timedelta(0.25), y[i] - (y_max * 0.025))
                    ax.annotate(f'{y[i]}( +{((y[i] / y[i - 1]) - 1) * 100:3.2f}%)', xy=xy, fontsize=8)

        ax.grid(True)
        return

    def plot_data_and_fit(self, x: np.ndarray, offset_days: int, y: np.ndarray, y_fit: np.ndarray):
        x_1 = x[offset_days:]
        x_axis = mdates.date2num(x_1)
        fig, ax = plt.subplots()

        ax.plot(x_axis, y, 'o')

        x_axis = []
        x_axis[:len(x_1)] = x_1
        for i in range(len(x_1), np.size(y_fit)):
            x_axis.append(x_axis[i-1] + timedelta(days=1))
        ax.plot(x_axis, y_fit, '--')
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        ax.format_xdata = mdates.DateFormatter('%d-%m-%Y')

        ax.set_xlabel('Dates')
        ax.set_ylabel('Data and Fit')
        fig.autofmt_xdate()
        ax.grid(True)

        return


if __name__ == "__main__":
    print('Cannot run file!!!')
