import requests
import pandas as pd
import csv


url = 'http://mip-prod-web.azurewebsites.net/InstantaneousViewFileDownload/DownloadFile'

resp = requests.get(url)
raw_csv = resp.content.decode('utf-8')

cr = csv.reader(raw_csv.splitlines(), delimiter=',')
data_list = list(cr)
labels = data_list[0]
data = data_list[1:]
df = pd.DataFrame.from_records(data, columns=labels)

df = df[(df['Expired (Y/N)'] == 'Y') | (df['Expired (Y/N)'] == 'N')]

df = df.pivot(index='Timestamp', columns='System Entry Name', values='Value')

print(df)
print(df.dtypes)



