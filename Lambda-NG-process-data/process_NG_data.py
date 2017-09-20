import csv
import os

import boto3
from datetime import datetime
from Flow_ORM import Base
from Flow_ORM import Flow
import Connection
from sqlalchemy.orm import sessionmaker

rds_endpoint = os.getenv('RDS_Instance_Endpoint')

def lambda_handler(event, context):
    test_sns_topic_arn = os.environ['Test_SNS_Topic_ARN']
    try:
        engine = Connection.get_db_engine(rds_endpoint)

        Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        session = Session()

        message = event['Records'][0]['Sns']['Message']
        records = message_to_records(message)
        for r in records:
            timestamp = str(r['Timestamp'])
            location = r['System Entry Name']
            value = r['Value']
            id = timestamp + ' ' + location
            new_flow = Flow(id=id, timestamp=timestamp, location=location, value=value)
            session.merge(new_flow)

        session.commit()
        session.close()
        engine.dispose()

    except Exception as e:
        error_msg = str(e)
        publish_result(test_sns_topic_arn, error_msg)


def publish_result(test_sns_topic_arn, message):
    message_to_pub = "DATABASE ERROR\n\n" + message
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
