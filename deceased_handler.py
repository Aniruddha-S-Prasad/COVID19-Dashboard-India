import requests
import csv


class DeceasedHandler:

    def __init__(self):
        self.database_filename = 'databases/deceased.csv'
        try:
            open(self.database_filename, 'r').close()
        except FileNotFoundError:
            response = requests.get("https://api.covid19india.org/states_daily_csv/deceased.csv")
            if response is None:
                print('Get request to https://api.covid19india.org/states_daily_csv/deceased.csv failed!!!')
                raise IOError
            else:
                with open(self.database_filename, 'w') as deceased_csv:
                    deceased_csv.write(response.text)

    def load_csv_data(self, state: str) -> dict:
        with open(self.database_filename, 'r') as deceased_csv:
            output = {}
            reader = csv.DictReader(deceased_csv)
            for row in reader:
                output[row['date']] = row[state]
        return output


if __name__ == '__main__':
    print('Cannot run file!!!')
