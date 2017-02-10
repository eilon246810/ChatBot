from model import *

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

datas=session.query(Data).all()

for i in datas:
	for a in i.adjectives:
		print i.noun+': '+a.adjective