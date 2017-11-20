import requests
import boto3
import os

def lambda_handler(event, context):
    url = os.getenv('Norway_URL')
    url2 = os.getenv('Norway_URL_2')
    sns_topic_arn = os.getenv('SNS_Topic_ARN')
    data = get_data(url, url2)
    return send_data(sns_topic_arn, data)


def get_data(url, url2):
    resp = requests.get(url)
    cookie = resp.cookies
    resp2 = requests.get(url=url2, allow_redirects=True, cookies=cookie)
    data_string = resp2.content.decode('utf-8')

    return data_string
    '''
    soup = BeautifulSoup(data_string, 'html.parser')
    flows = soup.findAll("td", class_= "flow")
    for f in flows:
        heading = f.find("div", class_="heading").string
        value = float(f.find("div", class_="value").string)
        print(heading, value)
    '''

def send_data(sns_topic_arn, data_string):

    sns = boto3.client('sns')

    sns.publish(TargetArn=sns_topic_arn,
                Message=data_string
                )
    return data_string

