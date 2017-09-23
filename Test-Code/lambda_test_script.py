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

    url = "https://53h0uj4c71.execute-api.eu-west-2.amazonaws.com/beta/gas"
    data = {"grid": "GTS", "type":"location", "location": "ZEVENAAR"}

    resp = requests.post(url=url, json=data)

    resp_content = eval(resp.content.decode("utf-8"))

    pprint(resp_content)

query_via_api()