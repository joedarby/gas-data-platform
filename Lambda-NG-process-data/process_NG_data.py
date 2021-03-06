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

        Insert_Records.insert(records, "NG", rds_endpoint)

    except Exception as e:
        error_msg = str(e)
        publish_error(error_msg)


def publish_error(message):
    message_to_pub = "DATABASE ERROR - NG\n\n" + message
    sns = boto3.client('sns')
    sns.publish(TargetArn=sns_error_arn,
                Message=message_to_pub)


def message_to_records(message):
    cr = csv.reader(message.splitlines(), delimiter=',')
    data_list = list(cr)
    records = []

    for row in data_list[1:]:
        if (row[4] == 'Y') or (row[4] == 'N'):
            name = row[0]
            value = float(row[2])
            timestamp = row[3]
            timestamp_dt = datetime.strptime(timestamp, '%d/%m/%Y %H:%M:%S')
            record = {'Timestamp': timestamp_dt, 'Location': name, 'Value': value}

            records.append(record)

    return records
