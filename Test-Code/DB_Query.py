import sqlalchemy
import sys

sys.path.insert(0, '/home/joe/PycharmProjects/gas-data-platform/Lambda-NG-process-data')
import rds_config

rds_host = 'gasdb.csomj93pkcws.eu-west-2.rds.amazonaws.com'
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

connection_string = "mysql+pymysql://" + name + ":" + password + "@" + rds_host + "/" + db_name + "?connect_timeout=20"
engine = sqlalchemy.create_engine(connection_string, echo=True)

conn = engine.connect()

res = conn.execute("SELECT * FROM NGData")

for r in res:
    print(r)

conn.close()
engine.dispose()