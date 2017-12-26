import os

#from DB_Tools import Connection
#from DB_Tools import Flow_ORM
#from DB_Tools import ng_mapping
import Connection
#import Flow_ORM
import ng_mapping
#from pprint import pprint


rds_endpoint = os.getenv('RDS_Instance_Endpoint')

def lambda_handler(event, context):

    try :

        #eventBody = eval(event['body'])
        #eventBody = event['body']
        engine = Connection.get_db_engine(rds_endpoint)
        results = get_results(engine)
        response = create_response(results)
        engine.dispose()

        return response

    except Exception as e:

        return {"statusCode": 500, "headers": {"Content-Type": "application/json"}, "body": str(e)}


def get_results(engine):

    # query_gas_grid = eventBody['grid']
    #
    # if query_gas_grid == "NG":
    #     table = Flow_ORM.NG_Flow.__tablename__
    # elif query_gas_grid == "GTS":
    #     table = Flow_ORM.GTS_Flow.__tablename__
    # else:
    #     table = Flow_ORM.Norway_Flow.__tablename__

    query = "SELECT a.timestamp, a.location, a.value, a.direction " \
                  "FROM %s a " \
                  "INNER JOIN (" \
                  "     SELECT location, value, direction, MAX(timestamp) timestamp " \
                  "     FROM %s " \
                  "     GROUP BY location " \
                  ") b ON a.location = b.location AND a.timestamp = b.timestamp" % ("GTSData", "GTSData")

    return engine.execute(query)


def create_response(results):

    if results:
        terminals = {}

        for r in results:
            location = r.location
            timestamp = r.timestamp.strftime('%d/%m/%Y %H:%M')
            value = r.value if r.direction == 'Entry' else -r.value

            if location in ng_mapping.GTS_terminal_map.keys():
                p = ng_mapping.Pipeline(location, value, timestamp)
                t = ng_mapping.GTS_terminal_map[location]
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
