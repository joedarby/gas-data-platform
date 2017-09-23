import csv
import os

import boto3
from datetime import datetime
import Insert_Records

rds_endpoint = os.getenv('RDS_Instance_Endpoint')
sns_error_arn = os.environ['SNS_Error_ARN']


def lambda_handler(event, context):
    try:
        message = event['Records'][0]['Sns']['Message']
        records = message_to_records(message)

        Insert_Records.insert(records, "GTS", rds_endpoint)

    except Exception as e:
        error_msg = str(e)
        publish_error(error_msg)


def publish_error(message):
    message_to_pub = "DATABASE ERROR - GTS\n\n" + message
    sns = boto3.client('sns')
    sns.publish(TargetArn=sns_error_arn,
                Message=message_to_pub)


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
