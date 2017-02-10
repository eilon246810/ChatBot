from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func

from datetime import datetime

Base = declarative_base()

class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    text=Column(String)
    kind=Column(String)
    is_input=Column(Boolean)

engine = create_engine('sqlite:///data.db')


Base.metadata.create_all(engine)