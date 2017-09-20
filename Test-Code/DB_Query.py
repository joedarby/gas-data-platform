import sqlalchemy
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_
from datetime import datetime

sys.path.insert(0, '/home/joe/PycharmProjects/gas-data-platform/DB_Tools')
import Connection
from Flow_ORM import Flow

rds_endpoint = 'gasdb.csomj93pkcws.eu-west-2.rds.amazonaws.com'

def lambda_handler(event, context)

engine = Connection.get_db_engine(rds_endpoint)

Session = sessionmaker(bind=engine)
session = Session()

#results = session.query(Flow).filter(and_(Flow.location == 'ALDBROUGH', Flow.timestamp < datetime(2017,9,20,16,45)))
results = session.query(Flow).filter(or_(Flow.location == 'ALDBROUGH', Flow.location == "HILLTOP"))

for r in results:
    print(r.timestamp, " ", r.location, "\t", r.value)

print("\n\n")
session.close()
engine.dispose()