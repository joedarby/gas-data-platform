import sys
import requests
from pprint import pprint

sys.path.insert(0, '/home/joe/PycharmProjects/gas-data-platform/Lambda-API-Query')
sys.path.insert(1, '/home/joe/PycharmProjects/gas-data-platform/DB_Tools')

import query_data

def query_directly():
    event = {'body': "{'type':'location', 'location':'ALDBROUGH'}"}
    output = query_data.lambda_handler(event, None)
    pprint(output)

def query_via_api():

    #url = "https://wjvfbfyc7c.execute-api.eu-west-2.amazonaws.com/dev/lambda_handler"
    url = "https://wjvfbfyc7c.execute-api.eu-west-2.amazonaws.com/dev/last_vals"
    #data = {"grid": "Norway", "type":"timeframe", "from":"23/12/2017 23:00"}
    #data = {"grid": "Norway", "type": "no_filter"}
    data = {"grid": "NG"}

    resp = requests.post(url=url, json=data)

    resp_content = eval(resp.content.decode("utf-8"))

    pprint(resp_content)

query_via_api()
