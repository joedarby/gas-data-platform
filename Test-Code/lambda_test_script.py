import sys
import requests
from pprint import pprint
import json

sys.path.insert(0, '/home/joe/PycharmProjects/gas-data-platform/Lambda-API-Query')
sys.path.insert(1, '/home/joe/PycharmProjects/gas-data-platform/DB_Tools')

import query_data

def query_directly():
    event = {'body': "{'grid': 'GTS', 'type':'no_filter'}"}
    query_data.lambda_handler(event, None)


def query_via_api():

    url = "https://53h0uj4c71.execute-api.eu-west-2.amazonaws.com/beta/gas"
    data = {'grid': 'GTS', 'type': 'no_filter'}

    resp = requests.post(url=url, json=data)

    resp_content = eval(resp.content.decode("utf-8"))

    pprint(resp_content)

query_via_api()
