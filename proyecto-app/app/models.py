from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from dataclasses import dataclass

Base = declarative_base()

class TopProduct(Base):
    __tablename__ = 'topproduct'

    advertiser_id = Column(String, primary_key=True)
    product_id = Column(String, primary_key=True)
    top_product = Column(Integer)
    date = Column(Date)

class TopCTR(Base):
    __tablename__ = 'topctr'

    advertiser_id = Column(String, primary_key=True)
    product_id = Column(String, primary_key=True)
    ctr = Column(Integer)
    date = Column(Date)
