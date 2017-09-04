import os
import boto3

def lambda_handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    test_sns_topic_arn = os.environ['Test_SNS_Topic_ARN']
    publish_result(test_sns_topic_arn, message)


def publish_result(test_snsn_topic_arn, message):
    sns = boto3.client('sns')
    sns.publish(TargetArn=test_snsn_topic_arn,
                Message=message)