import Connection
from sqlalchemy.orm import sessionmaker
import Flow_ORM

def insert(records, gas_grid, rds_endpoint):
    engine = Connection.get_db_engine(rds_endpoint)

    Session = sessionmaker(bind=engine)
    Flow_ORM.Base.metadata.create_all(engine)
    session = Session()

    for r in records:
        timestamp = str(r['Timestamp'])
        location = r['Location']
        value = r['Value']
        id = timestamp + ' ' + location

        if gas_grid == "GTS":
            direction = r['Direction']
            new_flow = Flow_ORM.GTS_Flow(id=id, timestamp=timestamp, location=location, value=value, direction=direction)
        elif gas_grid == "NG":
            new_flow = Flow_ORM.NG_Flow(id=id, timestamp=timestamp, location=location, value=value)
        elif gas_grid == "Norway":
            new_flow = Flow_ORM.Norway_Flow(id=id, timestamp=timestamp, location=location, value=value)
        session.merge(new_flow)

    session.commit()
    session.close()
    engine.dispose()
