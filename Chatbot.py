from random import *
import string

from model import *
engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

all_words=session.query(Word).all()

kinds=[]

for word in all_words:
    if word.kind not in kinds:
        kinds.append(word.kind)

data={}
for kind in kinds:
    #print kind
    #exec('global '+kind)
    #exec(str(kind)+'=[word.text for word in session.query(Word).filter_by(kind=kind).all()]')
    #print eval(kind)
    data[kind]=[word.text for word in session.query(Word).filter_by(kind=kind).all()]

'''global greetings
global questions
global answers
global goodbyes
global exits
greetings=[greet.text for greet in session.query(Word).filter_by(kind='greetings').all()] #imporve
questions=[quest.text for quest in session.query(Word).filter_by(kind='questions').all()] #imporve
answers=[answer.text for answer in session.query(Word).filter_by(kind='answers').all()] #imporve
goodbyes=[bye.text for bye in session.query(Word).filter_by(kind='goodbyes').all()] #imporve
exits=[exit.text for exit in session.query(Word).filter_by(kind='exits').all()] #imporve

data={'greetings' : greetings, 'questions' : questions, 'answers' : answers} #imporve'''
global input_data
input_data={}

for kind in data:
    exec(str(kind)+'=[word.text for word in session.query(Word).filter_by(kind=kind).all()]')
#print info
def process_input(s):
    s=s.lower()
    if not s.isalpha():
        # if there is a '
        for letter in range(len(s)):
            if s[letter]=='\'':
                if s[letter+1]=='s':
                    s=s.replace(s[letter:letter+2],' is')
                elif s[letter+1]=='m':
                    s=s.replace(s[letter:letter+2],' am')
                elif s[letter+1:letter+3]=='re':
                    s=s.replace(s[letter:letter+3],' are')
        
        for letter in range(len(s)):
            #print "'"+s[letter-1:+letter+2]+"'"
            if s[letter] in string.punctuation and s[letter] not in "' ".split():    
                s=s.replace(s[letter],' ')
        for letter in range(len(s)):
            short=s[letter-1:+letter+2]
            if short==' r ':
                s=s.replace(short,' are ')
            if s[letter-1:+letter+2]==' u ':
                s=s.replace(short,' you ')
            if s[letter-1:+letter+2]==' n ':
                s=s.replace(short,' and ')
    for word in s.split():
        if word in 'doin'.split():
            s=s.replace(word,word+'g')

    s=s.split()
    print s
    return s

def random_capitalized_answer(list_of_answers):
    answer=choice(list_of_answers).capitalize()
    return answer

def get_subjects(userInput):
    subjects={}
    for word in range(len(userInput)):
        if userInput[word] in 'how what who when why'.split():
            print '#@$'
            return {}
        if userInput[word] in 'you'.split():
            subjects[str(word)]='bot'
        elif userInput[word] in 'i'.split():
            subjects[str(word)]='human'
        elif userInput[word] in 'they she it he'.split():
            subjects[str(word)]='someone_else'
    print 'subjects: '+str(subjects)
    return subjects

def mine_data(userInput):
    for word in range(len(userInput)):
        if userInput[word] in 'is are am'.split():
            if userInput[word]=='am':
                input_data['human']=userInput[word+1:]
            elif userInput[word] in'is are'.split():
                input_data[userInput[word-1]]=userInput[word+1:]
    print input_data
def separate_sentences(userInput,subjects):
    sentences_subjects={}
    l=list(subjects.keys())
    for i in range(len(l)):
        try:
            #print userInput[int(l[i]):int(l[i+1])]
            sentences_subjects[str(i)+' '+str(userInput[int(l[i]):int(l[i+1])])]=subjects[l[i]]
        except:
            sentences_subjects[str(i)+' '+str(userInput[int(l[i]):])]=subjects[l[i]]
    print 'sentences subects: '+str(sentences_subjects)
    return sentences_subjects

def generate_responses(userInput,subject):
    if userInput[0] in exits:
        print random_capitalized_answer(goodbyes)
        return '!#@BREAK@#!'
    if userInput[0] in 'help info'.split():
        return [info[0]]
    if userInput==[]:
        return ['Please write some words here...']
    
    responses=[]
    stop=False
    if subject=='human':
        response= 'I know nothing about you...'
    elif subject=='someone_else':
        response= userInput[0]+' is not really '+userInput[2:]
    else:
        print '!@#else'
        for i in range(len(userInput)):
            word=userInput[i]
            if word in 'how what who when why'.split(): #if question
                word=''
                for w in userInput[i:]:
                    word+=w+' '
                word=word[:-1]
                #userInput=userInput[:i]
                stop=True

            if word in curses:
                response=word.capitalize()+'?! '+ random_capitalized_answer(offended)
            elif word in greetings:
                response= random_capitalized_answer(greetings)
            elif word in questions:
                response = random_capitalized_answer(answers)
                response+='. And how are you?'
            else:
                response='\\\\ I didn\'t understand what you meant in \"'+word+'\"'
            responses.append(response)
            if stop:
                break
        return responses
    responses.append(response)
    return responses




print '\n\t@ Hello! It\'s Eilon\'s Chatbot!\n\t  Please type "help" if you need some ;)'


while True:
    userInput = process_input(raw_input(">>> "))
    print('')
    mine_data(userInput)
    subjects=get_subjects(userInput)
    #responses=generate_responses(userInput)
    responses=[]
    if responses=='!#@BREAK@#!':
        break

    userInput_without=userInput

    if  subjects=={}:
        print 'subjects=={}'
        responses=generate_responses(userInput_without,'else')

    else:
        if userInput_without==[]:
            print 'OK'
            #continue
        sentences_subjects=separate_sentences(userInput,subjects)
        for sentence in sentences_subjects:
            sentence_words=eval(sentence[2:])
            print userInput_without, sentence_words
            for word in sentence_words:
                userInput_without.remove(word)        

        #print userInput_without
        responses=generate_responses(userInput_without,'else')

        for sentence in sentences_subjects:
            sentence_words=eval(sentence[2:])
            subject=sentences_subjects[sentence]
            responses+=generate_responses(sentence_words,subject)
            print subject
        #continue
    print '\t@ '+responses[0]
    for response in responses[1:]:
        print '\t  '+response
    print('')