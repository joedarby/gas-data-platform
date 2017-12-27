import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_
from datetime import datetime

import Connection
import Flow_ORM

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
    response = create_response(results)

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


def create_response(results):

    if results:
        data = {}
        for r in results:
            location = r.location
            timestamp = r.timestamp
            value = r.value
            if hasattr(r, "direction"):
                direction = r.direction
            else:
                direction = "Entry"
            time = timestamp.timestamp()
            if location not in data.keys():
                data[location] = {}
            data[location][time] = value if direction == "Entry" else -value

        data_wrapped = {"dataList": data}

        response = {"statusCode": 200, "headers": {"Content-Type": "application/json"}, "body": str(data_wrapped)}
    else:
        response = {"statusCode": 404, "headers": {"Content-Type": "application/json"}}

    return response
