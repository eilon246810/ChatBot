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

class Data(Base):
	__tablename__ = 'data'
	id = Column(Integer, primary_key=True)
	noun=Column(String)
	adjectives=relationship("Adjective", back_populates="data")

class Adjective(Base):
    __tablename__ = 'adjective'
    id = Column(Integer, primary_key=True)
    adjective=Column(String)
    data_id = Column(Integer, ForeignKey('data.id'))
    data = relationship("Data", back_populates="adjectives")
		
engine = create_engine('sqlite:///data.db')


Base.metadata.create_all(engine)