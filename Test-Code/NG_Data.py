import requests
from My_bs4 import My_bs4
from datetime import datetime
import pytz


def get_data(url, url2):
    resp = requests.get(url)
    cookie = resp.cookies
    resp2 = requests.get(url=url2, allow_redirects=True, cookies=cookie)
    data_string = resp2.content.decode('utf-8')

    return data_string


def message_to_records(message):
    soup = My_bs4.BeautifulSoup(message, 'html.parser')
    update_time_string = soup.find("div", class_="lastUpdate").string[-19:]
    timestamp_dt = datetime.strptime(update_time_string, '%Y-%m-%d %H:%M:%S')
    timestamp_dt = pytz.timezone('Europe/Oslo').localize(timestamp_dt)
    flows = soup.findAll("td", class_="flow")

    records = []

    for f in flows:
        heading = f.find("div", class_="heading").string
        value = float(f.find("div", class_="value").string)
        record = {'Timestamp': timestamp_dt, 'Location': heading, 'Value': value}
        records.append(record)

    return records

url2 = "http://flow.gassco.no/acceptDisclaimer"
url = "http://flow.gassco.no/"

data = get_data(url, url2)
result = message_to_records(data)

for r in result:
    print(r)




