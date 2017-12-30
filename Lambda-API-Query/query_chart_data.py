import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_
from datetime import datetime

#from DB_Tools import Connection, Flow_ORM, ng_mapping
import Connection
import Flow_ORM
import ng_mapping
#from pprint import pprint

rds_endpoint = os.getenv('RDS_Instance_Endpoint')

def lambda_handler(event, context):

    locations = event['queryStringParameters']['location'].split(',')
    country = event['queryStringParameters']['country']
    timeFrom = event['queryStringParameters']['timeFrom']
    timeTo = event['queryStringParameters']['timeTo']


    engine = Connection.get_db_engine(rds_endpoint)
    Session = sessionmaker(bind=engine)
    session = Session()

    results = get_results(session, locations, country, timeFrom, timeTo)
    response = create_response(results, country)

    session.close()
    engine.dispose()

    return {"statusCode": 200, "headers": {"Content-Type": "application/json"}, "body": str(response)}


def get_results(session, locations, country, timeFrom, timeTo):

    if country == "uk":
        flow_class = Flow_ORM.NG_Flow
    elif country == "nl":
        flow_class = Flow_ORM.GTS_Flow
    else:
        flow_class = Flow_ORM.Norway_Flow

    queryFrom_dt = datetime.strptime(timeFrom, '%d/%m/%Y %H:%M')
    queryTo_dt = datetime.strptime(timeTo, '%d/%m/%Y %H:%M')

    if locations[0] == "all":
        results = session.query(flow_class).filter(
            and_(flow_class.timestamp >= queryFrom_dt,
                 flow_class.timestamp <= queryTo_dt,
                 )
        )
    else:
        results = session.query(flow_class).filter(
            and_(flow_class.timestamp >= queryFrom_dt,
                 flow_class.timestamp <= queryTo_dt,
                 flow_class.location.in_(locations)
                 )
        )

    return results


def create_response(results, country):

    if results:

        temp_terminal_map = {}
        for r in results:
            location = r.location
            direction = r.direction if hasattr(r, "direction") else "Entry"
            value = r.value if direction == "Entry" else -r.value
            time = r.timestamp.timestamp()
            terminal_name = ng_mapping.get_terminal_name(country, location)

            if terminal_name not in temp_terminal_map.keys():
                temp_terminal_map[terminal_name] = {}
            if location not in temp_terminal_map[terminal_name].keys():
                temp_terminal_map[terminal_name][location] = {}
            temp_terminal_map[terminal_name][location][time] = value

        terminals = []
        for tName in temp_terminal_map.keys():
            if tName:
                terminal = {"terminalName": tName,
                            "pipelines": []}
                for pName in temp_terminal_map[tName].keys():
                    pipeline = {"pipelineName": pName,
                                "data": temp_terminal_map[tName][pName]
                                }
                    terminal["pipelines"].append(pipeline)

                terminals.append(terminal)

        data_wrapped = {"dataList": terminals}

        response = data_wrapped

        #response = {"statusCode": 200, "headers": {"Content-Type": "application/json"}, "body": str(data_wrapped)}
    else:
        response = {"statusCode": 404, "headers": {"Content-Type": "application/json"}}

    return response

# test_event = {"queryStringParameters": {"location": "all",
#                                         "country": "uk",
#                                         "timeFrom": "30/12/2017 13:00",
#                                         "timeTo": "30/12/2017 13:12"
#                                         }
#               }
# pprint(lambda_handler(test_event, ""))



