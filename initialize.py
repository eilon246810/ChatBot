from model import *

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

session.query(Word).delete()
session.query(Data).delete()
session.query(Adjective).delete()

nouns=['human','bot']
for noun in nouns:
	new_data=Data(noun=noun)
	session.add(new_data)
input_data={
	'greetings' : ['hola', 'hello', 'hi','hey'],

	'questions' : ['how are you','how are you doing','sup','what is up'],

	'exits':['exit', 'quit', 'bye'],

	'curses':['stupid', 'idiot'],
}

output_data={
	'answers' : ['i\'m okay','i\'m fine', 'just fine', 'grate'],

	'goodbyes' : ['bye!','see ya!','come back later!','chow!'],

	'offended': ['no! you are!', 'shut up!', 'i\'m offended.', 'GIVE IT BACK!'],
}


info_commands={
	'Help':'View this help messege',
	}

info_messege='''Hello, I\'m Eilon\'s Chatbot.

\t  My commands are:\n
'''
# Command Info
i=1
for command in info_commands:
	info_messege+='\t  '+str(i)+'. '+command
	for x in range(len(max(info_messege, key=len))+15-len(command)):
		info_messege+=' '
	info_messege+=info_commands[command]+'.\n'
	i+=1

# Input Info
i=1
info_messege+='\n\t  Things You Can Say:\n'
for data in input_data:
	info_messege+='\t  '+str(i)+'. '+data+':'
	for x in range(len(max(info_messege, key=len))+14-len(data)):
		info_messege+=' '
	info_messege+=str(input_data[data])+'.\n'
	i+=1

# Output Info
i=1
info_messege+='\n\t  Things I Can Say:\n'
for data in output_data:
	info_messege+='\t  '+str(i)+'. '+data
	for x in range(len(max(info_messege, key=len))+15-len(data)):
		info_messege+=' '
	info_messege+=str(output_data[data])+'.\n'
	i+=1

info_messege=Word(text=info_messege,kind='info',is_input=True)
session.add(info_messege)

for kind in input_data.keys():
	for i in input_data[kind]:
		word=Word(text=i,kind=kind,is_input=True)
		session.add(word)

for kind in output_data.keys():
	for i in output_data[kind]:
		word=Word(text=i,kind=kind,is_input=False)
		session.add(word)

session.commit()