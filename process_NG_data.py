import os
import sys
import boto3
import rds_config
import pymysql
import logging
import csv
import pandas as pd
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from Flow_ORM import Flow
from Flow_ORM import Base

pd.set_option('display.width', 9999)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#rds_host = os.getenv('RDS_Instance_Endpoint')
rds_host = 'rds-mysql-10mintutorial.csomj93pkcws.eu-west-2.rds.amazonaws.com'
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

connection_string = "mysql+pymysql://" + name + ":" + password + "@" + rds_host + "/" + db_name

engine = sqlalchemy.create_engine(connection_string, echo=True)

Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()


def lambda_handler(event, context):
    message = event['Records'][0]['sns']['message']
    #test_sns_topic_arn = os.environ['Test_SNS_Topic_ARN']
    #publish_result(test_sns_topic_arn, message)

    df = message_to_dataframe(message)
    records = df.to_dict('records')
    for r in records:
        timestamp = str(r['Timestamp'])
        location = r['System Entry Name']
        value = r['Value']
        id = timestamp + ' ' + location
        new_flow = Flow(id=id, timestamp=timestamp, location=location, value=value)
        session.merge(new_flow)

    session.commit()


    connection = engine.connect()
    result = connection.execute("select * from ORMTest2 WHERE timestamp>'2017-09-19 00:15:00' AND location='ALDBROUGH'")
    for row in result:
        print(row)
    connection.close()


def publish_result(test_snsn_topic_arn, message):
    sns = boto3.client('sns')
    sns.publish(TargetArn=test_snsn_topic_arn,
                Message=message)

def message_to_dataframe(message):
    cr = csv.reader(message.splitlines(), delimiter=',')
    data_list = list(cr)
    labels = data_list[0]
    data = data_list[1:]
    df = pd.DataFrame.from_records(data, columns=labels)

    df = df[(df['Expired (Y/N)'] == 'Y') | (df['Expired (Y/N)'] == 'N')]
    df = df[['Timestamp', 'System Entry Name', 'Value']]
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Value'] = pd.to_numeric(df['Value'])

    #df = df.pivot(index='Timestamp', columns='System Entry Name', values='Value')


    #print(df)
    #print(df.dtypes)

    return df