import csv
import os

import boto3
import rds_config
import sqlalchemy
from datetime import datetime
from Flow_ORM import Base
from Flow_ORM import Flow
from sqlalchemy.orm import sessionmaker

rds_host = os.getenv('RDS_Instance_Endpoint')
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

connection_string = "mysql+pymysql://" + name + ":" + password + "@" + rds_host + "/" + db_name
engine = sqlalchemy.create_engine(connection_string, echo=True)

Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()


def lambda_handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    test_sns_topic_arn = os.environ['Test_SNS_Topic_ARN']

    records = message_to_records(message)
    for r in records:
        timestamp = str(r['Timestamp'])
        location = r['System Entry Name']
        value = r['Value']
        id = timestamp + ' ' + location
        new_flow = Flow(id=id, timestamp=timestamp, location=location, value=value)
        session.merge(new_flow)

    session.commit()

    publish_result(test_sns_topic_arn, message)


def publish_result(test_sns_topic_arn, message):
    message_to_pub = "DATABASE UPDATED\n\n" + message
    sns = boto3.client('sns')
    sns.publish(TargetArn=test_sns_topic_arn,
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
            record = {'Timestamp': timestamp_dt, 'System Entry Name': name, 'Value': value}

            records.append(record)

    return records
