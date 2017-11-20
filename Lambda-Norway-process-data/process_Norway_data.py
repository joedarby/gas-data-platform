import os

import boto3
from datetime import datetime
import Insert_Records
import pytz
from My_bs4 import BeautifulSoup

rds_endpoint = os.getenv('RDS_Instance_Endpoint')
sns_error_arn = os.environ['SNS_Error_ARN']


def lambda_handler(event, context):

    try:
        message = event['Records'][0]['Sns']['Message']
        records = message_to_records(message)

        Insert_Records.insert(records, "Norway", rds_endpoint)

    except Exception as e:
        error_msg = str(e)
        publish_error(error_msg)


def publish_error(message):
    message_to_pub = "DATABASE ERROR - Norway\n\n" + message
    sns = boto3.client('sns')
    sns.publish(TargetArn=sns_error_arn,
                Message=message_to_pub)


def message_to_records(message):
    soup = BeautifulSoup(message, 'html.parser')
    update_time_string = soup.find("div", class_="lastUpdate").string[-19:]
    timestamp_dt = datetime.strptime(update_time_string, '%Y-%m-%d %H:%M:%S')
    timestamp_dt = pytz.timezone('Europe/Oslo').localize(timestamp_dt)
    flows = soup.findAll("td", class_="flow")

    records = []

    for f in flows:
        heading = f.find("div", class_="heading").string
        value = float(f.find("div", class_="value").string)
        record = {'Timestamp': timestamp_dt, 'Location': heading, 'Value': value}
        records.append(record)

    return records
