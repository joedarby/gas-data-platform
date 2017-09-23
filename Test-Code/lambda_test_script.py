import sys
import csv
from datetime import datetime

sys.path.insert(0, '/home/joe/PycharmProjects/gas-data-platform/Lambda-GTS-get-file')
sys.path.insert(1, '/home/joe/PycharmProjects/gas-data-platform/DB_Tools')

import get_GTS_data
import Flow_ORM

group = {'Bocholtz TENP': '01',
              'Bocholtz Vetschau': '02',
              'Dinxperlo': '03'}

vs, vsg, ev, cookie, = get_GTS_data.establish_connection()
message = get_GTS_data.get_csv_data(group, vs, vsg, ev, cookie)


def message_to_records(message):
    cr = csv.reader(message.splitlines(), delimiter=',')
    data_list = list(cr)
    records = []

    for row in data_list[4:-1]:
        name = row[1]
        if row[3] == '':
            direction = "Exit"
            value = int(row[4])
        else:
            direction = "Entry"
            value = int(row[3])
        timestamp = row[2]
        timestamp_dt = datetime.strptime(timestamp, '%d-%m-%Y %H:%M')
        record = {'Timestamp': timestamp_dt, 'Location': name, 'Value': value, 'Direction': direction}
        print(record)

        records.append(record)

    return records

message_to_records(message)