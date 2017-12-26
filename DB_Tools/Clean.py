import Connection
import os
from pprint import pprint

rds_endpoint = os.getenv('RDS_Instance_Endpoint')

print(rds_endpoint)

engine = Connection.get_db_engine(rds_endpoint)

sql_string = "SELECT location, ROUND(AVG(value), 2) AS 'val'"  \
             "FROM NorwayData " \
             "WHERE timestamp > '2017-12-01 00:00'" \
             "GROUP BY location"

sql_string2 = "SELECT MAX(timestamp), value " \
              "FROM NGData "





result = engine.execute(sql_string3)

for line in result:
    pprint(line)