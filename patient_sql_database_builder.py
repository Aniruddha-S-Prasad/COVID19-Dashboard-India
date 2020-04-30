import json
import requests
import sqlite3

database_filename = 'databases/patients.db'


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
    c.execute("""CREATE TABLE IF NOT EXISTS patients (
                    patientnumber INTEGER PRIMARY KEY,
                    dateannounced TEXT,
                    statecode TEXT,
                    currentstatus TEXT,
                    detecteddistrict TEXT,
                    detectedstate TEXT,
                    agebracket INTEGER)
                    """)
    connection.commit()
    return


def insert_patient(connection, patient):
    if connection is None:
        raise TypeError

    c = connection.cursor()
    try:
        c.execute("""SELECT * FROM patients WHERE patientnumber=:patientnumber""", patient)
    except sqlite3.ProgrammingError:
        print(patient)
        raise RuntimeError

    if len(c.fetchall()) == 0:
        try:
            c.execute("""INSERT INTO patients VALUES (
                            :patientnumber,
                            :dateannounced,
                            :statecode,
                            :currentstatus,
                            :detecteddistrict,
                            :detectedstate,
                            :agebracket)""", patient)
        except sqlite3.IntegrityError:
            print('What the Fuck???')
            return 1
        return 0
    else:
        return 1


def create_deaths_recoveries_table(connection):
    if connection is None:
        raise TypeError

    c = connection.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS deaths_recoveries (
                    slno INTEGER PRIMARY KEY,
                    date TEXT,
                    patientstatus TEXT,
                    statecode TEXT,
                    state TEXT)
                    """)
    connection.commit()
    return


def insert_deaths_recoveries_data(connection, patient):
    if connection is None:
        raise TypeError

    c = connection.cursor()
    try:
        c.execute("""SELECT * FROM deaths_recoveries WHERE slno=:slno""", patient)
    except sqlite3.ProgrammingError:
        print(patient)
        raise RuntimeError

    if len(c.fetchall()) == 0:
        try:
            c.execute("""INSERT INTO deaths_recoveries VALUES (
                            :slno,
                            :date,
                            :patientstatus,
                            :statecode,
                            :state)""", patient)
        except sqlite3.IntegrityError:
            print('What the Fuck???')
            return 1
        return 0
    else:
        return 1


def download_and_load(url: str) -> list:

    with open('databases/raw_data1.json', 'r', encoding='utf-8') as data_file1:
        raw_data1_json = json.load(data_file1)

    with open('databases/raw_data2.json', 'r', encoding='utf-8') as data_file2:
        raw_data2_json = json.load(data_file2)

    try:
        with open('databases/raw_data.json', 'r', encoding='utf-8') as data_file:
            raw_data_json = json.load(data_file)
    except FileNotFoundError:
        raw_data_response = requests.get(url)
        raw_data_json = json.loads(raw_data_response.text)
        with open('databases/raw_data.json', 'w', encoding='utf-8') as data_file:
            json.dump(raw_data_json, data_file, ensure_ascii=False, indent=4)

    raw_data_list = raw_data1_json['raw_data'] + raw_data2_json['raw_data'] + raw_data_json['raw_data']

    return raw_data_list


def main():

    url = 'https://api.covid19india.org/raw_data3.json'
    raw_data_list = download_and_load(url)

    conn = create_connection()
    create_patients_table(conn)

    patients_added = 0

    for raw_data_person in raw_data_list:
        try:
            if insert_patient(conn, raw_data_person) == 0:
                patients_added += 1
                # print(patients_added)
        except RuntimeError:
            print(patients_added)
            print(raw_data_person['patientnumber'])
            raise RuntimeError
    conn.commit()

    print(f"Added {patients_added} patients!")

    conn.close()
    return 0


if __name__ == "__main__":
    main()
