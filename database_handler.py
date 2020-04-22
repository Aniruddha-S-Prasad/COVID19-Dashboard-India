# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:37:38 2020

@author: Aniruddha-S-Prasad
"""
import deceased_handler
import recovered_handler
import sqlite3
import numpy as np
from datetime import datetime, date, timedelta


class DatabaseHandler:
    """
    The DatabaseHandler class consists of all methods required to interface with the COVID-19 database.
    This class uses SQLite3 to query the database. The methods in this class strive to be injection safe
    """

    def __init__(self, from_date: date, to_date: date, state='IN'):
        """
        Class constructor, initialises the date_strings required to query the database
        date_strings is a list containing strings of the form "dd/mm/YYYY"
        :param from_date: Start date for the SQL query
        :param to_date: End date for the SQL query
        """
        self.date_strings = []
        self.date_strings_alternate = []

        h = to_date - from_date
        month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        for num_days in range(h.days + 1):
            current_day = from_date + timedelta(days=num_days)
            current_day_string = f'{current_day.day:02d}/{current_day.month:02d}/{current_day.year:04d}'
            current_day_string_alternate = f'{current_day.day:02d}-{month[current_day.month-1]}-{current_day.year%100}'
            self.date_strings.append(current_day_string)
            self.date_strings_alternate.append(current_day_string_alternate)

        self.dates, self.total_count = self.get_total_count(state=state, cumulative=True)
        _, self.recovered_count = self.get_recovered_count(state=state, cumulative=True)
        _, self.deceased_count = self.get_deceased_count(state=state, cumulative=True)

    def get_total_count(self, state='IN', cumulative=True, sql_conn=None):
        if sql_conn is None:
            connection = self.__create_connection()
            cursor = connection.cursor()
            conn_created = True
        else:
            conn_created = False
            cursor = sql_conn.cursor()

        count = np.zeros(len(self.date_strings))
        dates = []

        for index, date_string in enumerate(self.date_strings):
            dates.append(datetime.strptime(date_string, '%d/%m/%Y'))

            if state == 'IN':
                cursor.execute("""SELECT COUNT(*) FROM patients 
                                    WHERE dateannounced=?""", (date_string,))
            else:
                cursor.execute("""SELECT COUNT(*) FROM patients 
                                    WHERE dateannounced=? AND statecode=?""", (date_string, state))

            count[index] = (cursor.fetchone()[0])
        if conn_created:
            connection.close()

        if cumulative:
            for i in range(1, len(count)):
                count[i] = count[i] + count[i - 1]

        return dates, count

    def get_recovered_count(self, state='IN', cumulative=True):
        if state == 'IN':
            state = 'TT'

        dates = []
        count = np.zeros(len(self.date_strings_alternate))

        handler = recovered_handler.RecoveredHandler()
        data_dict = handler.load_csv_data(state)

        for index, date_string in enumerate(self.date_strings_alternate):
            try:
                count[index] = data_dict[date_string]
            except KeyError:
                count[index] = 0

        if cumulative:
            for i in range(1, len(count)):
                count[i] = count[i] + count[i - 1]

        for date_string in self.date_strings:
            dates.append(datetime.strptime(date_string, '%d/%m/%Y'))

        return dates, count

    def get_deceased_count(self, state='IN', cumulative=True):
        if state == 'IN':
            state = 'TT'

        dates = []
        count = np.zeros(len(self.date_strings_alternate))

        handler = deceased_handler.DeceasedHandler()
        data_dict = handler.load_csv_data(state)

        for index, date_string in enumerate(self.date_strings_alternate):
            try:
                count[index] = data_dict[date_string]
            except KeyError:
                count[index] = 0

        if cumulative:
            for i in range(1, len(count)):
                count[i] = count[i] + count[i - 1]

        for date_string in self.date_strings:
            dates.append(datetime.strptime(date_string, '%d/%m/%Y'))

        return dates, count

    def get_removed_count(self, state='IN', cumulative=True):
        dates, recovered = self.get_recovered_count(state, cumulative)
        tmp, deceased = self.get_deceased_count(state, cumulative)
        removed_count = recovered + deceased
        return dates, removed_count

    def __create_connection(self, database_filename='patients.db'):
        connection = None
        try:
            connection = sqlite3.connect(database_filename)
            return connection
        except Exception as error:
            print(error)
        return connection


if __name__ == '__main__':
    print('Cannot run file!!!')
