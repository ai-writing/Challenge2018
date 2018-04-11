f = open("../data/data.conll","r")
ftext = open("../data/text.txt","w")
sentence_ID = 0
last_word = ''
words = []
POS = []
father = []
link = []
Dict = {}
for line in f.readlines():
    word = line.split()
    if len(word)==0:
        continue
    if word[0]=='1':
        sentence_ID+=1
        for each in words:
            print >>ftext, each,
        print >>ftext
        words = []
        POS = []
        father = []
        link = []
        last_word = ''
    word1 = word[1].lower()
    words.append(word[1])
    POS.append(word[3])
    father.append(int(word[5]))
    link.append(word[6])
    if (not Dict.has_key(word1)):
        Dict[ word1 ] = 0
    if last_word == 'a':
        Dict[ word1 ] |= 1
    if last_word == 'an':
        Dict[ word1 ] |= 2
    if last_word == 'the':
        Dict[ word1 ] |= 4
    last_word = word1
f = open("../data/word_article.txt", "w")
for each in Dict:
    print >>f, each,Dict[each]
