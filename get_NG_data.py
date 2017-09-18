import requests
import boto3
import os

def lambda_handler(event, context):
    #url = os.environ['NG_Terminal_URL']
    url = 'http://mip-prod-web.azurewebsites.net/InstantaneousViewFileDownload/DownloadFile'
    #sns_topic_arn = os.environ['SNS_Topic_ARN']
    sns_topic_arn = 'null'
    return get_and_send_data(url, sns_topic_arn)

def get_and_send_data(url, sns_topic_arn):

    resp = requests.get(url)
    data_string = resp.content.decode('utf-8')

    #sns = boto3.client('sns')

    #sns.publish(TargetArn=sns_topic_arn,
    #            Message=data_string
    #            )
    return data_string



