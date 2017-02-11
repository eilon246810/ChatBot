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

datas=session.query(Data).all()

for i in datas:
    input_data[i.noun]=[]
    for a in i.adjectives:
        input_data[i.noun].append(a.adjective)


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
    print 'proceed: '+str(s) #debugging
    return s

def random_capitalized_answer(list_of_answers):
    answer=choice(list_of_answers).capitalize()
    return answer

def get_subjects(userInput):
    subjects={}
    for word in range(len(userInput)):
        if userInput[word] in 'how what who when why'.split():
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
    mined_data=False
    new_data_mined=False
    for word in range(len(userInput)):
        if userInput[word] in 'is are am'.split() and word!=0:
            adjective=''.join(data+' ' for data in userInput[word+1:])[:-1]
            if adjective=='':
                continue

            if userInput[word-1] in 'how what who when why'.split():
                continue

            for w in range(len(adjective.split())-1):
                if adjective.split()[w] in 'am is are'.split():
                    adjective=''.join(i+' ' for i in adjective.split()[:w-1])[:-1]

            if userInput[word]=='am': #human
                if adjective not in input_data['human']:
                    input_data['human'].append(adjective)
                    noun='human'
                    new_data_mined=True

            elif userInput[word] in 'is are'.split():
                if userInput[word-1][0:] in 'you bot'.split(): #bot
                    if adjective not in input_data['bot']:
                        input_data['bot'].append(adjective)
                        noun='bot'
                        data_id=session.query(Data).filter_by(noun=noun)
                        new_data_mined=True

                else: #else
                    if userInput[word-1] not in input_data:
                        input_data[userInput[word-1]]=[]
                        input_data[userInput[word-1]].append(adjective)
                        noun=userInput[word-1]
                        new_data=Data(noun=noun)
                        session.add(new_data)
                        session.commit()
                        new_data_mined=True
                    else:
                        if adjective not in input_data[userInput[word-1]]:
                            input_data[userInput[word-1]].append(adjective)
                            noun=''.join(i+' ' for i in userInput[word-1].split())[:-1]
                            print 'noun: '+noun
                            new_data_mined=True
            
            mined_data=True
            if new_data_mined:
                if adjective!='':
                    data_id=session.query(Data).filter_by(noun=noun).one().id
                    adjective=Adjective(adjective=adjective,data_id=data_id)
                    session.add(adjective)
    session.commit()
    return mined_data

def separate_sentences(userInput,subjects):
    sentences_subjects={}
    l=list(subjects.keys())
    for i in range(len(l)):
        try:
            #print userInput[int(l[i]):int(l[i+1])]
            sentences_subjects[str(i)+' '+str(userInput[int(l[i]):int(l[i+1])])]=subjects[l[i]]
        except:
            sentences_subjects[str(i)+' '+str(userInput[int(l[i]):])]=subjects[l[i]]
    return sentences_subjects

def generate_responses(userInput,subject,mined_data):
    if userInput==[]:
        return ['Please write some words here...']
    if mined_data:
        return ['Good to know that!']
    if userInput[0] in exits:
        print random_capitalized_answer(goodbyes)
        return '!#@BREAK@#!'
    if userInput[0] in 'help info'.split():
        return [info[0]]
    
    did_not_undertstand_allowed=True

    responses=[]
    stop=False
    if subject=='human':
        response= 'Good to know that!'
    else:
        for i in range(len(userInput)):
            word=userInput[i]
            if word in 'how who when why what'.split(): #if question
                word=''
                for w in userInput[i:]:
                    word+=w+' '
                word=word[:-1]
                #userInput=userInput[:i]
                stop=True
            
            if word in 'what'.split():
                did_not_undertstand_allowed=False
            
            if word in input_data or word in 'you me'.split():
                if word in 'me i'.split():
                    word='human'
                elif word=='you':
                    word='bot'

                if input_data[word]==[]:
                    if word[-1]=='s' and word[-2]!='s':
                        response='I don\'t know anything about '+word+'.'
                    elif word[-1] in 's o x z'.split() or word[-2:] in 'ch sh ss'.split():
                        response='I don\'t know anything about '+word+'es.'
                    elif word[-1] in 'y'.split() and word[-2] not in 'a e i o u'.split():
                        response='I don\'t know anything about '+word+'ies.'
                    else:
                        response='I don\'t know anything about '+word+'s.'
                    responses.append(response)
                    continue

                if word in 'she he'.split():
                    response=word+' is: '+''.join(data+', ' for data in input_data[word])[:-2]+'.'
                elif word[-1]=='s' and word[-2]!='s' or word in 'we they'.split():
                    response=word+' are: '+''.join(data+', ' for data in input_data[word])[:-2]+'.'
                elif word[-1] in 's o x z'.split() or word[-2:] in 'ch sh ss'.split():
                    response=word+'es are: '+''.join(data+', ' for data in input_data[word])[:-2]+'.'
                elif word[-1] in 'y'.split() and word[-2] not in 'a e i o u'.split():
                    response=word+'ies are: '+''.join(data+', ' for data in input_data[word])[:-2]+'.'
                else:
                    response=word+'s are: '+''.join(data+', ' for data in input_data[word])[:-2]+'.'
            elif word in curses:
                response=word.capitalize()+'?! '+ random_capitalized_answer(offended)
            elif word in greetings:
                response= random_capitalized_answer(greetings)
            elif word in questions:
                response = random_capitalized_answer(answers)
                response+='. And how are you?'
            else:
                if did_not_undertstand_allowed:
                    response='\\\\ I didn\'t understand what you meant in \"'+word+'\"'
            responses.append(response)
            if stop:
                break
        return responses
    responses.append(response)
    return responses




print '\n\t@ Hello! It\'s Eilon\'s Chatbot!\n\t  Please type "help" if you need some ;)'

def main():
    while True:
        userInput = process_input(raw_input(">>> "))
        print('')
        mined_data=mine_data(userInput)
        subjects=get_subjects(userInput)
        #responses=generate_responses(userInput)
        responses=[]

        userInput_without=userInput

        if  subjects=={}:
            responses=generate_responses(userInput_without,'else',mined_data)

        else:
            if userInput_without==[]:
                print 'OK'
                #continue
            sentences_subjects=separate_sentences(userInput,subjects)
            for sentence in sentences_subjects:
                sentence_words=eval(sentence[2:])
                for word in sentence_words:
                    userInput_without.remove(word)        

            #print userInput_without
            #responses=generate_responses(userInput_without,'else',mined_data)

        if responses=='!#@BREAK@#!':
            break

            for sentence in sentences_subjects:
                sentence_words=eval(sentence[2:])
                subject=sentences_subjects[sentence]
                responses+=generate_responses(sentence_words,subject,mined_data)
                print 'subject: '+str(subject)
        print 'input_data: '+str(input_data)
            #continue
        print '\t@ '+responses[0]
        for response in responses[1:]:
            print '\t  '+response
        print('')

if __name__ == '__main__':
    main()