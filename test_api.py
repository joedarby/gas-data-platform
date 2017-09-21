import requests
from pprint import pprint

url = 'https://53h0uj4c71.execute-api.eu-west-2.amazonaws.com/beta/gas'
test = {"type": "location", "location": "ALDBROUGH"}

resp = requests.post(url=url, json=test)

resp_string = resp.content.decode("utf-8")
resp_dict = eval(resp_string)

print(resp.reason)

pprint(resp_dict)