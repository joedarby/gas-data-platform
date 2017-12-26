#from DB_Tools import rds_config
import rds_config
import sqlalchemy

def get_db_engine(rds_endpoint):
    name = rds_config.db_username
    password = rds_config.db_password
    db_name = rds_config.db_name

    connection_string = "mysql+pymysql://" + name + ":" + password + "@" + rds_endpoint + "/" + db_name

    engine = sqlalchemy.create_engine(connection_string, echo=True)

    return engine