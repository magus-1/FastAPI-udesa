from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TopProduct(Base):
    __tablename__ = 'topproduct'

    id = Column(Integer, primary_key=True)
    advertiser_id = Column(String)
    product_id = Column(String)
    top_product = Column(Integer)
    date = Column(Date)
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TopProduct(Base):
    __tablename__ = 'topproduct'

    id = Column(Integer, primary_key=True)
    advertiser_id = Column(String)
    product_id = Column(String)
    top_product = Column(Integer)
    date = Column(Date)

class TopCTR(Base):
    __tablename__ = 'topctr'

    id = Column(Integer, primary_key=True)
    advertiser_id = Column(String)
    product_id = Column(String)
    ctr = Column(Integer)
    date = Column(Date)

class Stats(Base):
    __tablename__ = 'stats'

    id = Column(Integer, primary_key=True)
    advertiser_id = Column(String)
    impressions = Column(Integer)
    clicks = Column(Integer)
    conversions = Column(Integer)

class Stats(Base):
    __tablename__ = 'stats'

    id = Column(Integer, primary_key=True)
    advertiser_id = Column(String)
    impressions = Column(Integer)
    clicks = Column(Integer)
    conversions = Column(Integer)