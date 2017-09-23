import requests
import boto3
import os
import sys


pointCodes = [{'Bocholtz TENP': '01',
              'Bocholtz Vetschau': '02',
              'Dinxperlo': '03'},
              {'Emden EPT':'04',
              'Emden NPT': '05',
              'Haanrade': '06'},
              {'Hilvarenbeek': '07',
              'Julianadorp': '08',
              'Obbicht': '09'},
              {'Oude Gascade': '10',
              'Oude GTG Nord': '11',
              'Oude GUD-G': '12'},
              {'Oude GUD-H': '13',
              'Oude OGE': '14',
              'S-Grav': '15'},
              {'Tegelen': '16',
              'Vlieghuis': '17',
              'Winterswijk': '18'},
              {'Zandvliet-G': '19',
              'Zandvliet-H': '20',
              'Zelzate': '21'},
              {'Zevenaar': '22',
              'Zone Oude Statenzijl': '23'
              }]

#sns_topic_arn = os.getenv('SNS_Topic_ARN')
#sns_error_arn = os.getenv('SNS_Error_ARN')
sns_topic_arn = "arn:aws:sns:eu-west-2:451093560309:GTS_Terminals"
sns_error_arn = "arn:aws:sns:eu-west-2:451093560309:NG_test"

def lambda_handler(event, context):
    vs, vsg, ev, cookie, = establish_connection()
    for group in pointCodes:
        try_count = 0
        while try_count < 3:
            try:
                raw_csv = get_csv_data(group, vs, vsg, ev, cookie)
                publish_to_sns(raw_csv)
                break
            except Exception as e:
                try_count += 1
                if try_count == 3:
                    publish_error(str(e))


def establish_connection():
    try_count = 0
    error = ""
    while try_count < 3:
        try:
            viewState, viewStateGenerator, eventValidation, cookie = first_request()
            return viewState, viewStateGenerator, eventValidation, cookie
        except Exception as e:
            try_count += 1
            error = str(e)
            continue
    publish_error(error)
    sys.exit()

def get_csv_data(points, viewState, viewStateGenerator, eventValidation, cookie):
    pointCodeDict = get_point_code_dict(points)
    rs, ci = second_request(viewState, viewStateGenerator, eventValidation, cookie, pointCodeDict)
    raw_csv = third_request(rs, ci, cookie)

    return raw_csv


def publish_to_sns(data_string):
    sns = boto3.client('sns')

    sns.publish(TargetArn=sns_topic_arn,
                Message=data_string
                )


def publish_error(message):
    message_to_pub = "GTS DOWNLOAD ERROR\n\n" + message
    sns = boto3.client('sns')
    sns.publish(TargetArn=sns_error_arn,
                Message=message_to_pub)


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

    resp = requests.get(url = url, params=params, headers = headers)
    content = str(resp.content)
    cookie = resp.cookies.get_dict()
    ViewState = content.split("id=\"__VIEWSTATE\" value=\"", 1)[1].split("\"", 1)[0]
    ViewStateGenerator = content.split("id=\"__VIEWSTATEGENERATOR\" value=\"", 1)[1].split("\"", 1)[0]
    EventValidation = content.split("id=\"__EVENTVALIDATION\" value=\"", 1)[1].split("\"", 1)[0]

    print("First request complete")

    return ViewState, ViewStateGenerator, EventValidation, cookie


def second_request(ViewState, ViewStateGenerator, EventValidation, cookie, pointCodeDict):
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
               'Connection': 'keep-alive'
               }

    resp = requests.post(url=url, cookies=cookie, params=params, data=form_data, headers= headers)

    content = str(resp.content)

    rs = content.split("ReportSession=", 1)[1].split("u002", 1)[0][:-2]
    ci =  content.split("ControlID=", 1)[1].split("u002", 1)[0][:-2]

    print("Second request complete")

    return rs, ci

def third_request(ReportSession, ControlID, cookie):
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
    print("third request complete")

    return content


def get_point_code_dict(pointDict):

    keyString = 'ReportViewerControl$ctl04$ctl05$divDropDown$ctl'

    pointCodeDict = {}

    for point in pointDict.keys():
        code = pointDict.get(point)
        key = keyString + code
        pointCodeDict[key] = 'on'

    return pointCodeDict


