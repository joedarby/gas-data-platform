import os

#from DB_Tools import Connection
#from DB_Tools import Flow_ORM
#from DB_Tools import ng_mapping
import Connection
import Flow_ORM
import ng_mapping
#from pprint import pprint


rds_endpoint = os.getenv('RDS_Instance_Endpoint')

def lambda_handler(event, context):

    try :
        country = event['queryStringParameters']['country']
        engine = Connection.get_db_engine(rds_endpoint)
        results = get_results(engine, country)
        response = create_response(results, country)
        engine.dispose()

        return response

    except Exception as e:

        return {"statusCode": 500, "headers": {"Content-Type": "application/json"}, "body": str(e)}


def get_results(engine, country):

    if country == "uk":
        table = Flow_ORM.NG_Flow.__tablename__
        dir = ""
        dir2 = ""
    elif country == "nl":
        table = Flow_ORM.GTS_Flow.__tablename__
        dir = ", a.direction"
        dir2 = "direction, "
    else:
        table = Flow_ORM.Norway_Flow.__tablename__
        dir = ""
        dir2 = ""


    query = "SELECT a.timestamp, a.location, a.value%s " \
                  "FROM %s a " \
                  "INNER JOIN (" \
                  "     SELECT location, value, %sMAX(timestamp) timestamp " \
                  "     FROM %s " \
                  "     GROUP BY location " \
                  ") b ON a.location = b.location AND a.timestamp = b.timestamp" % (dir, table, dir2, table)

    return engine.execute(query)


def create_response(results, country):

    if country == "uk":
        tMap = ng_mapping.NG_terminal_map
    elif country == "nl":
        tMap = ng_mapping.GTS_terminal_map
    else:
        tMap = None

    if results:
        terminals = {}

        for r in results:
            location = r.location
            timestamp = r.timestamp.strftime('%d/%m/%Y %H:%M')
            direction = r.direction if hasattr(r, "direction") else "Entry"
            value = r.value if direction == "Entry" else -r.value

            p = ng_mapping.Pipeline(location, value, timestamp)
            if tMap is None:
                t = location
                terminals[t] = ng_mapping.Terminal(t)
                terminals[t].add_pipeline(p)

            elif location in tMap.keys():
                t = tMap[location]
                if t not in terminals:
                    terminals[t] = ng_mapping.Terminal(t)
                terminals[t].add_pipeline(p)

        terminals_json = [t.to_json() for t in terminals.values()]

        response = {"statusCode": 200, "headers": {"Content-Type": "application/json"}, "body": str(terminals_json)}
    else:
        response = {"statusCode": 404, "headers": {"Content-Type": "application/json"}}

    return response


#event = {"body": {"grid": "NG"}}

#pprint(lambda_handler("", ""))
