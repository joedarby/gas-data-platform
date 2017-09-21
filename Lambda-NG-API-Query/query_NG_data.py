import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_
from datetime import datetime
import json

import Connection
from Flow_ORM import Flow

rds_endpoint = os.getenv('RDS_Instance_Endpoint')

def lambda_handler(event, context):
    engine = Connection.get_db_engine(rds_endpoint)
    Session = sessionmaker(bind=engine)
    session = Session()

    eventBody = eval(event['body'])

    queryType = eventBody['type']
    results = None

    if queryType == "no_filter":
        results = session.query(Flow)
    elif queryType == "location":
        queryLocation = eventBody['location']
        results = session.query(Flow).filter(Flow.location == queryLocation)
    elif queryType == "timeframe":
        queryFrom = eventBody["from"] if "from" in eventBody else None
        queryFrom_dt = datetime.strptime(queryFrom, '%d/%m/%Y %H:%M') if queryFrom else None
        queryTo = eventBody["to"] if "to" in eventBody else None
        queryTo_dt = datetime.strptime(queryTo, '%d/%m/%Y %H:%M') if queryTo else None
        if queryFrom and queryTo:
            results = session.query(Flow).filter(and_(Flow.timestamp >= queryFrom_dt, Flow.timestamp <= queryTo_dt))
        elif queryFrom:
            results = session.query(Flow).filter(Flow.timestamp >= queryFrom_dt)
        elif queryTo:
            results = session.query(Flow).filter(Flow.timestamp <= queryTo_dt)

    if results:
        response= {}
        for r in results:
            location = r.location
            timestamp = r.timestamp
            value = r.value
            time = timestamp.strftime('%d/%m/%Y %H:%M')
            if location in response.keys():
                response[location][time] = value
            else:
                response[location] = {}
                response[location][time] = value
        outputJson = {"statusCode": 200, "headers": {"Content-Type": "application/json"}, "body": str(response)}
    else:
        outputJson = {"statusCode": 404, "headers": {"Content-Type": "application/json"}}

    session.close()
    engine.dispose()

    return outputJson
