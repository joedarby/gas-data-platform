import json, requests
from pprint import pprint

url = 'https://transparency.entsog.eu/api/v1/operationaldatas?'

params = ["periodType=hour",
    '&from=2017-08-28',
    '&to=2017-08-29',
    '&operatorKey=NL-TSO-0001',
    '&indicator=Physical Flow',
    '&periodize=1',
    '&limit=100',
    '&pointLabel=Zevenaar',
    '&direction=exit',
    '&sort=Period'
    ]

for p in params:
    url += p

resp = requests.get(url=url)
data = json.loads(resp.text)['operationaldatas']

for i in data:
    print(i['periodFrom'][:17], i['value'])

