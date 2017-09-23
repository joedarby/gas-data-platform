import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_
from datetime import datetime

import Connection
import Flow_ORM

rds_endpoint = os.getenv('RDS_Instance_Endpoint')

def lambda_handler(event, context):

    eventBody = eval(event['body'])

    engine = Connection.get_db_engine(rds_endpoint)
    Session = sessionmaker(bind=engine)
    session = Session()

    results = get_results(eventBody, session)
    response = create_response(results)

    session.close()
    engine.dispose()

    return response


def get_results(eventBody, session):


    query_gas_grid = eventBody['grid']
    queryType = eventBody['type']
    results = None

    flow_class = Flow_ORM.NG_Flow if query_gas_grid == "NG" else Flow_ORM.GTS_Flow

    if queryType == "no_filter":
        results = session.query(flow_class)
    elif queryType == "location":
        queryLocation = eventBody['location']
        results = session.query(flow_class).filter(flow_class.location == queryLocation)
    elif queryType == "timeframe":
        queryFrom = eventBody["from"] if "from" in eventBody else None
        queryFrom_dt = datetime.strptime(queryFrom, '%d/%m/%Y %H:%M') if queryFrom else None
        queryTo = eventBody["to"] if "to" in eventBody else None
        queryTo_dt = datetime.strptime(queryTo, '%d/%m/%Y %H:%M') if queryTo else None
        if queryFrom and queryTo:
            results = session.query(flow_class).filter(and_(flow_class.timestamp >= queryFrom_dt, flow_class.timestamp <= queryTo_dt))
        elif queryFrom:
            results = session.query(flow_class).filter(flow_class.timestamp >= queryFrom_dt)
        elif queryTo:
            results = session.query(flow_class).filter(flow_class.timestamp <= queryTo_dt)

    return results


def create_response(results):

    if results:
        response= {}
        for r in results:
            location = r.location
            timestamp = r.timestamp
            value = r.value
            if hasattr(r, "direction"):
                direction = r.direction
            else:
                direction = "Entry"
            time = timestamp.strftime('%d/%m/%Y %H:%M')
            if location in response.keys():
                response[location][time] = {direction: value}
            else:
                response[location] = {}
                response[location][time] = {direction: value}
        outputJson = {"statusCode": 200, "headers": {"Content-Type": "application/json"}, "body": str(response)}
    else:
        outputJson = {"statusCode": 404, "headers": {"Content-Type": "application/json"}}

    return outputJson