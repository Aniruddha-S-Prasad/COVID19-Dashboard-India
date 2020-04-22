import json
import requests
import sqlite3

database_filename = 'recoveries_and_deaths.db'


def create_connection():
    connection = None
    try:
        connection = sqlite3.connect(database_filename)
        return connection
    except Exception as e:
        print(e)
    return connection


def create_patients_table(connection):
    if connection is None:
        raise TypeError

    c = connection.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS recoveries_and_deaths (
                    slno INTEGER PRIMARY KEY,
                    date TEXT,
                    patientstatus TEXT,
                    district TEXT,
                    state TEXT,
                    statecode TEXT,
                    agebracket INTEGER)
                    """)
    connection.commit()
    return


def insert_patient(connection, patient):
    if connection is None:
        raise TypeError

    c = connection.cursor()
    c.execute("""SELECT * FROM recoveries_and_deaths WHERE slno=:slno""", patient)

    if len(c.fetchall()) == 0:
        c.execute("""INSERT INTO recoveries_and_deaths VALUES (
                        :slno,
                        :date,
                        :patientstatus,
                        :district,
                        :state,
                        :statecode,
                        :agebracket)""", patient)
        return 0
    else:
        return 1


def main():
    try:
        with open('recoveries_and_deaths.json', 'r', encoding='utf-8') as data_file:
            raw_data_json = json.load(data_file)

    except FileNotFoundError:
        # Get raw data response from api, response in json
        raw_data_response = requests.get('https://api.covid19india.org/deaths_recoveries.json')
        # json.loads = json.load'string'
        raw_data_json = json.loads(raw_data_response.text)
        with open('recoveries_and_deaths.json', 'w', encoding='utf-8') as data_file:
            json.dump(raw_data_json, data_file, ensure_ascii=False, indent=4)

    # Response contains a key value of {'raw_data':'{COMPLETE_DATA_SET}'}
    # COMPLETE_DATA_SET contains individual data of patients in a list of dicts

    raw_data_list = raw_data_json['deaths_recoveries']
    conn = create_connection()
    create_patients_table(conn)

    patients_added = 0

    for raw_data_person in raw_data_list:
        if insert_patient(conn, raw_data_person) == 0:
            patients_added += 1
    conn.commit()

    print(f"Added {patients_added} people")

    conn.close()
    return 0


if __name__ == "__main__":
    main()
