from sqlalchemy.ext .declarative import declarative_base
from sqlalchemy import Column, TIMESTAMP, CHAR, FLOAT, INTEGER

Base = declarative_base()

class NG_Flow(Base):
    __tablename__ = 'NGData'

    id = Column(CHAR(60), primary_key=True)
    timestamp = Column(TIMESTAMP)
    location = Column(CHAR(30))
    value = Column(FLOAT)


class GTS_Flow(Base):
    __tablename__ = 'GTSData'

    id = Column(CHAR(80), primary_key=True)
    timestamp = Column(TIMESTAMP)
    location = Column(CHAR(50))
    value = Column(INTEGER)
    direction = Column(CHAR(10))


class Norway_Flow(Base):
    __tablename__ = 'NorwayData'

    id = Column(CHAR(80), primary_key=True)
    timestamp = Column(TIMESTAMP)
    location = Column(CHAR(30))
    value = Column(FLOAT)
