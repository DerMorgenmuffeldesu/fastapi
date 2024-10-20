from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Advertisement(Base):
    __tablename__ = 'advertisements'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    author = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    