import requests
import csv
import pandas as pd

cookie = {'ASP.NET_SessionId': 'clq2tye2r5f4csoyk4apagj3'}


def first_request():
    url = 'http://dataport.gastransportservices.nl/default.aspx'

    params = {'ReportPath': '/Transparency/FlowHsWobbePerNetworkpoint',
              'TransparencySegment': '01',
              'ReportTitle': 'FlowHsWobbePerNetworkpoint'}

    headers = {'Host': 'dataport.gastransportservices.nl',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Upgrade-Insecure-Requests': '1'
               }

    resp = requests.get(url = url, params=params, cookies = cookie, headers = headers)
    content = str(resp.content)
    ViewState = content.split("id=\"__VIEWSTATE\" value=\"", 1)[1].split("\"", 1)[0]
    ViewStateGenerator = content.split("id=\"__VIEWSTATEGENERATOR\" value=\"", 1)[1].split("\"", 1)[0]
    EventValidation = content.split("id=\"__EVENTVALIDATION\" value=\"", 1)[1].split("\"", 1)[0]

    print("First request complete")

    return ViewState, ViewStateGenerator, EventValidation


def second_request(ViewState, ViewStateGenerator, EventValidation, pointCodeDict):
    url = 'http://dataport.gastransportservices.nl/default.aspx'

    params = {'ReportPath': '/Transparency/FlowHsWobbePerNetworkpoint',
              'TransparencySegment': '01',
              'ReportTitle': 'FlowHsWobbePerNetworkpoint'}

    form_data = {'__EVENTTARGET': '',
                 '__EVENTARGUMENT':'',
                 '__VIEWSTATE': ViewState,
                 '__VIEWSTATEGENERATOR': ViewStateGenerator,
                 '__EVENTVALIDATION': EventValidation,
                 'ReportViewerControl$ctl03$ctl00':'',
                 'ReportViewerControl$ctl03$ctl01':'',
                 'ReportViewerControl$ctl10': '',
                 'ReportViewerControl$ctl11': 'standards',
                 'ReportViewerControl$AsyncWait$HiddenCancelField': 'False',
                 'ReportViewerControl$ctl04$ctl03$txtValue': 'Border points',
                 'ReportViewerControl$ctl04$ctl05$txtValue': 'BOCHOLTZ TENP (OGE - FLX TENP) - 300139; BOCHOLTZ VETSCHAU (THYSSENGAS) - 301368; DINXPERLO (BEW) - 300140; EMDEN EPT (GASSCO) - 301113; EMDEN NPT (GASSCO) - 301112; HAANRADE (THYSSENGAS) - 300141; HILVARENBEEK (FLUXYS) - 300131; JULIANADORP (BBL) - 301214; OBBICHT (FLUXYS) - 300137; OUDE STATENZIJL (GASCADE-H) - 300147; OUDE STATENZIJL (GTG NORD-G) - 300136; OUDE STATENZIJL (GUD-G)[OBEBG] - 300144; OUDE STATENZIJL (GUD-H)[OBEBH] - 300146; OUDE STATENZIJL (OGE) - 300145; S-GRAVENVOEREN (FLUXYS) - 300143; TEGELEN (OGE) - 300138; VLIEGHUIS (RWE) - 300142; WINTERSWIJK (OGE) - 300133; ZANDVLIET (FLUXYS-G) - 300134; ZANDVLIET (FLUXYS-H) - 301184; ZELZATE (FLUXYS) - 301111; ZEVENAAR - 300132; Zone Oude Statenzijl H - 301516',
                 'ReportViewerControl$ctl04$ctl07$ddValue': '1',
                 'ReportViewerControl$ctl04$ctl09$ddValue': '2',
                 'ReportViewerControl$ctl04$ctl00':'Apply',
                 'ReportViewerControl$ToggleParam$store':'',
                 'ReportViewerControl$ToggleParam$collapse':'false',
                 'ReportViewerControl$ctl08$ClientClickedId':'',
                 'ReportViewerControl$ctl07$store':'',
                 'ReportViewerControl$ctl07$collapse':'false',
                 'ReportViewerControl$ctl09$VisibilityState$ctl00':'None',
                 'ReportViewerControl$ctl09$ScrollPosition':'',
                 'ReportViewerControl$ctl09$ReportControl$ctl02':'',
                 'ReportViewerControl$ctl09$ReportControl$ctl03':'',
                 'ReportViewerControl$ctl09$ReportControl$ctl04':100
                 }

    form_data.update(pointCodeDict)

    headers = {'Host': 'dataport.gastransportservices.nl',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               }

    resp = requests.post(url=url, cookies=cookie, params=params, data=form_data, headers= headers)

    content = str(resp.content)

    rs = content.split("ReportSession=", 1)[1].split("u002", 1)[0][:-2]
    ci =  content.split("ControlID=", 1)[1].split("u002", 1)[0][:-2]

    print("Second request complete")

    return rs, ci

def third_request(ReportSession, ControlID):
    url = 'http://dataport.gastransportservices.nl/Reserved.ReportViewerWebControl.axd'\

    params = {
          'ReportSession': ReportSession,
          'Culture':1043,
          'CultureOverrides':True,
          'UICulture':1043,
          'UICultureOverrides':True,
          'ReportStack':1,
          'ControlID': ControlID,
          'OpType':'Export',
          'FileName':'FlowHsWobbePerNetworkpoint',
          'ContentDisposition':'OnlyHtmlInline',
          'Format':'CSV'

    }

    resp = requests.get(url=url, params=params, cookies=cookie)
    content = resp.content.decode('utf-8')

    return content


def get_dataframe(csv_content):

    cr = csv.reader(csv_content.splitlines(), delimiter=',')
    my_list = list(cr)
    labels = my_list[3]
    data = my_list[4:]

    df = pd.DataFrame.from_records(data, columns=labels)

    print(df)

def get_point_code_dict(pointStringList):

    pointCodes = {'Bocholtz TENP': '01',
              'Bocholtz Vetschau': '02',
              'Dinxperlo': '03',
              'Emden EPT':'04',
              'Emden NPT': '05',
              'Haanrade': '06',
              'Hilvarenbeek': '07',
              'Julianadorp': '08',
              'Obbicht': '09',
              'Oude Gascade': '10',
              'Oude GTG Nord': '11',
              'Oude GUD-G': '12',
              'Oude GUD-H': '13',
              'Oude OGE': '14',
              'S-Grav': '15',
              'Tegelen': '16',
              'Vlieghuis': '17',
              'Winterswijk': '18',
              'Zandvliet-G': '19',
              'Zandvliet-H': '20',
              'Zelzate': '21',
              'Zevenaar': '22',
              'Zone Oude Statenzijl': '23'
              }

    keyString = 'ReportViewerControl$ctl04$ctl05$divDropDown$ctl'

    pointCodeDict = {}

    for point in pointStringList:
        code = pointCodes.get(point)
        key = keyString + code
        pointCodeDict[key] = 'on'

    return pointCodeDict


points = ['Zevenaar', 'Hilvarenbeek', 'Zelzate']

pointCodeDict = get_point_code_dict(points)

ViewState, ViewStateGenerator, EventValidation = first_request()
rs, ci = second_request(ViewState, ViewStateGenerator, EventValidation, pointCodeDict)
raw_csv = third_request(rs, ci)
get_dataframe(raw_csv)
