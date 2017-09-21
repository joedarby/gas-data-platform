import requests
from pprint import pprint

url = 'https://53h0uj4c71.execute-api.eu-west-2.amazonaws.com/beta/gas'
test = {"type": "timeframe", "from": "21/09/2017 12:00", "to": "21/09/2017 14:00"}

resp = requests.post(url=url, json=test)

resp_string = resp.content.decode("utf-8")
resp_dict = eval(resp_string)

print(resp.reason)

pprint(resp_dict)