from sqlalchemy.ext .declarative import declarative_base
from sqlalchemy import Column, INTEGER, TIMESTAMP, CHAR, FLOAT

Base = declarative_base()

class Flow(Base):
    __tablename__ = 'NGData'

    id = Column(CHAR(60), primary_key=True)
    timestamp = Column(TIMESTAMP)
    location = Column(CHAR(30))
    value = Column(FLOAT)

