def test(f,n):
    sample_ngrams = {('is','an','example', '.'), ('this','is','an', 'example'), ('<go>', 'this','is','an'), ('','<go>','this','is'), ('','','<go>','this')}
    test_text = '\n**********\nYour input = {}\nYour output = {}\nYou {} the test this time!\n**********\n'
    tests_solutions = [
        ("Ca'/n4 you)$ .c$;3lean th@is?","can you clean this"),
        ('hows a baby formed','sorry i dont know much about a baby formed '),
        ('whats an aardvark','sorry i dont know much about an aardvark '),
        ('a skinny man','thanks, you skinny man !'),
        ('an extremely big elephant',"thanks, you extremely big elephant !"),
        ('theres nothing here!',None),
        ('this is an example', sample_ngrams),
        (sample_ngrams,['this']),
        (sample_ngrams,' this is an example .'),

    ]
    t,s= tests_solutions[n]
    r = f(t)
    print(test_text.format(t,r,['failed','passed'][r == s]))

#=========================
# CHATBOT PROJECT OBJECTIVES
#=========================
# make a chatbot which uses regex to look for key words or phrases and replies accordingly (bonus: mirroring the response)
# Bonus) for the default / unknown cases - have the bot generate sentences from trigrams (bonus: have it learn trigrams directly from user inputs)


# 1) =========================
# Clean a string of text from any punctuation, numbers and newlines and put all words into lower case
def clean(txt):
    cleaned = ''
    for letter in txt.lower():
        if ord('a') <= ord(letter) <= ord('z') or letter.isspace():
            cleaned += letter
    return cleaned.replace('\n',' ')
test(clean,0)

# 2) =========================
# Match patterns in a string using regex:
#   - Import Re
#   - write a regular expression to find the key word "what/s or how/s or when/s or why/s"
#   - write a regular expression to find the key word "a" or "an"
#   - use the re.search() function to look for all these patterns in a given string
#   - if a pattern is found also capture any words which occur after these words - e.g. "a" (man) <-- the word man is caught
#   - if no pattern is found, return None
#   - if more than one pattern is found, the pattern with highest priority should be returned ("whats" pattern is higher than "a" pattern in this case, )
#   - once found, return a string/reply associated to that pattern (- e.g. if the pattern for "what/s" is found, return the reply "sorry i dont know much about {}", and the reply "thanks, you {}!" for the "a" pattern
#   - in the blank {} left in the reply - fill it with the last word captured (e.g. "an aardvark! - thanks you {aardvark}")

def match_patterns(sentence):
    import re
    patterns = {
        r" (whats*|hows*|whens*|whys*) (.*)":"sorry i dont know much about {} .",
        r" an* (.*)":'thanks, you {} .',
    }
    for pattern,reply in patterns.items():
        objs = re.search(pattern,' ' + sentence + ' ')
        if objs is not None:
            last_obj = objs.groups()
            if len(last_obj) > 0 and last_obj[-1] is not None:
                last_obj = last_obj[-1]
            else:
                last_obj = ''
            return reply.format(last_obj)
test(match_patterns,1)
test(match_patterns,2)
test(match_patterns,3)
test(match_patterns,4)
test(match_patterns,5)

#3) =========================
# convert a string of words into a list of tuples containing three words each (called trigrams) 
# - e.g. this is a test -> [(this,is,a), (is,a,test),...]
#the string of words should start with a special token like "<go>" and end with a special token like "."
# at the very beginning, there should be a context word which will help connect the text to the previous sentence before
def text_to_ngrams(txt,context1 ='',context2 = '' ):
    ngrams = set()
    t = txt.split()
    txt = ['','','<go>'] + t + ['.']    
    for ngram in zip(txt,txt[1:],txt[2:],txt[3:]):
        ngrams.add(ngram)
    txt = [context1,context2,'<go>'] + t + ['.']
    for ngram in zip(txt,txt[1:],txt[2:],txt[3:]):
        ngrams.add(ngram)
    return ngrams

test(text_to_ngrams,6)

#4) =========================
# find all the trigrams which match a given first and second word
# return a list of just the third word for any trigram found
# if no trigrams are found and the list is empty - add a single '.' into it before returning

def find_ngrams(ngrams,first_word='',second_word='',third_word = '<go>'):
    quads = []
    for w1,w2,w3,w4 in ngrams:
        if w1 == first_word and w2 == second_word and w3 == third_word:
            quads.append(w4)
    if len(quads) == 0:
        quads.append('.')
    return quads
test(find_ngrams,7)

#5) =========================
# generate sentences using bigrams 
# use the special token <go> to start generating
# and the special token '.' to know when to stop the loop

def generate_sentence(ngrams, word1 = '',word2 = ''):
    from random import choice,shuffle
    generated = ''
    word3,word4 ='<go>',''
    while word4 != '.':
        words = find_ngrams(ngrams,word1,word2,word3)
        shuffle(words)
        word4 = choice(words)
        generated += ' ' + word4
        word1 = word2
        word2 = word3
        word3 = word4
        #print(word4)
    return generated

test(generate_sentence,8)

#6) =========================
# get last two words of a sentence
# return ['',''] if there isnt enough words in the sentence
def context(txt):
    t = txt.split()
    if len(t) >= 2:
        return t[-2:]
    elif len(t) >= 1:
        return ['', t[-1]]
    return ['','']

#7) =========================
#  ngram chatbot that can learn

def learn_and_talk(prev_user_sentence,pprev_bot_sentence,remembered_ngrams = set()):

    bot_context= clean(pprev_bot_sentence)
    user_context= clean(prev_user_sentence)

    bot_lastwords = context(bot_context)
    user_lastwords = context(user_context)

    remembered_ngrams |= text_to_ngrams(user_context, bot_lastwords[0], bot_lastwords[1])
    reply = generate_sentence(remembered_ngrams,user_lastwords[0], user_lastwords[1])

    if reply == ' .':
        reply = '(... lets change topic)\n' + generate_sentence(remembered_ngrams)
    return reply


# 8) =========================
def bootstrap_ngrams(filename):
    ngrams = set()
    last_words = ['','']
    with open(filename) as f:
        for lines in f.readlines():
            lines = lines.replace('!','\n').replace('?','\n').split('\n')
            for line in lines:
                txt = clean(line)
                ngrams |= text_to_ngrams(txt,last_words[0],last_words[1])
                last_words = context(txt)
    return ngrams

def save_to_file(ngrams):
    with open('ngrams.txt','w') as f:
        for w1,w2,w3,w4 in ngrams:
            f.write('{},{},{},{}\n'.format(w1,w2,w3,w4))

save_to_file(bootstrap_ngrams('shortjokes.csv'))

#9) =========================
# combining regex and ngram chabot

def chat():
    ngrams = set() #  bootstrap_ngrams('movies.txt')
    user,bot = 'hello',' .'
    while user != 'bye':
        user = input('user: ')
        reply = match_patterns(user)
        if reply is None:
            reply = learn_and_talk(user,bot,ngrams)
        print('bot:',reply)
        bot = reply
#chat()

