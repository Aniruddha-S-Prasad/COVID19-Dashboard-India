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
    c.execute("""SELECT * FROM patients WHERE patientnumber=:patientnumber""", patient)

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


def main():
    try:
        with open('databases/raw_data.json', 'r', encoding='utf-8') as data_file:
            raw_data_json = json.load(data_file)

    except FileNotFoundError:
        # Get raw data response from api, response in json
        raw_data_response = requests.get('https://api.covid19india.org/raw_data.json')
        # json.loads = json.load'string'
        raw_data_json = json.loads(raw_data_response.text)
        with open('databases/raw_data.json', 'w', encoding='utf-8') as data_file:
            json.dump(raw_data_json, data_file, ensure_ascii=False, indent=4)

    # Response contains a key value of {'raw_data':'{COMPLETE_DATA_SET}'}
    # COMPLETE_DATA_SET contains individual data of patients in a list of dicts

    raw_data_list = raw_data_json['raw_data']

    conn = create_connection()
    create_patients_table(conn)

    patients_added = 0

    for raw_data_person in raw_data_list:
        if insert_patient(conn, raw_data_person) == 0:
            patients_added += 1

    conn.commit()

    print(f"Added {patients_added} patients")

    conn.close()
    return 0


if __name__ == "__main__":
    main()
