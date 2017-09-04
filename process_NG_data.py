import os
import sys
import boto3
import rds_config
import pymysql
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

rds_host = os.environ['RDS_Instance_Endpoint']
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except Exception as e:
    logger.error("Unexpected error: could not connect to db instance")
    logger.exception(e)
    sys.exit()

logger.info("Successfully connected to db instance")

def lambda_handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    test_sns_topic_arn = os.environ['Test_SNS_Topic_ARN']
    #publish_result(test_sns_topic_arn, message)

    with conn.cursor() as cur:
        cur.execute("create table if not exists TestTable1 (PrimKey int NOT NULL, Thing varchar(255) NOT NULL, PRIMARY KEY (PrimKey))")
        cur.execute('insert into TestTable1 (PrimKey, Thing) values(1, "Hello")')
        cur.execute('insert into TestTable1 (PrimKey, Thing) values(2, "whats")')
        cur.execute('insert into TestTable1 (PrimKey, Thing) values(3, "up")')
        conn.commit()

        cur.execute("select * from TestTable1")
        for row in cur:
            print(row)

def publish_result(test_snsn_topic_arn, message):
    sns = boto3.client('sns')
    sns.publish(TargetArn=test_snsn_topic_arn,
                Message=message)