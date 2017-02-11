from model import *

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

datas=session.query(Data).all()

number_of_adjectives=0
for i in datas:
	for a in i.adjectives:
		number_of_adjectives+=1

print 'There are '+str(len(datas))+' nouns, with '+str(number_of_adjectives)+' adjectives.\n'

for i in datas:
	for a in i.adjectives:
		print i.noun+': '+a.adjective