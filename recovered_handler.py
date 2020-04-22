import requests
import csv


class RecoveredHandler:

    def __init__(self):
        self.database_filename = 'databases/recovered.csv'
        try:
            open(self.database_filename, 'r').close()
        except FileNotFoundError:
            response = requests.get("https://api.covid19india.org/states_daily_csv/recovered.csv")
            if response is None:
                print('Get request to https://api.covid19india.org/states_daily_csv/recovered.csv failed!!!')
                raise IOError
            else:
                with open(self.database_filename, 'w') as recovered_csv:
                    recovered_csv.write(response.text)

    def load_csv_data(self, state: str) -> dict:
        with open(self.database_filename, 'r') as recovered_csv:
            output = {}
            reader = csv.DictReader(recovered_csv)
            for row in reader:
                output[row['date']] = row[state]
        return output


if __name__ == '__main__':
    print('Cannot run file!!!')
