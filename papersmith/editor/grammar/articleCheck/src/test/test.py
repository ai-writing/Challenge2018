ORI_VALUE = 100
H_VALUE = 1000
WH_VALUE = 2000
WW_VALUE = 2000
P_VALUE = 500

le = []
ri = []
str = []
total_len = 0

#a an the ' '
def checkAvsAn(pos, begin):
    if Article[pos][0] and Article[pos][1]:
        if begin in a_words:
            Article[pos][1] = 0
            return
        if begin in an_words:
            Article[pos][0] = 0
            return
        if begin[0] in con_alph:
            Article[pos][1] = 0
        else:
            Article[pos][0] = 0

def checkTherebe(pos1,pos2):
    if words[pos1]=='is' or words[pos1]=='was' or words[pos1]=='be' or words[pos1]=='been':
        if words[pos2]=='there':
            return True
    return False

def articleChoose(pos,art):
    if pos!=0:
        if words[pos-1]==art:
            return
    if len(art)==0:
        if pos==0:
            return
        if words[pos-1]!='the' and words[pos-1]!='a' and words[pos-1]!='an':
            return
    if words[pos]=='-lrb-' or words[pos]=='-rrb-':
        return
    L = pos
    R = pos
    if pos!=0:
        if words[pos-1]=='a' or words[pos-1]=='an' or words[pos-1]=='the':
            L -= 1
    now_word = owords[pos]
    if pos==0:
        if (now_word[1:].islower() and now_word[0].isupper()):
            now_word=now_word[0].lower()+now_word[1:]
        if len(art)>0:
            art=art[0].upper()+art[1:]
    if art.lower()=='the':
        art = '('+art+')'
    le.append(total_len+L)
    ri.append(total_len+R)
    str.append(art+' '+now_word)
    #print(le, ri, art+' '+words[pos], file = fresult)

def PrintError():
    print('Print errors')
    print(file = fresult)
    for i in range(len(le)):
        print(le[i], ri[i], str[i], file = fresult)
    fresult.close()

os_path = "papersmith/editor/grammar/"
ftext = open(os_path+"articleCheck/data/test/text.txt","r")
fhead = open(os_path+"articleCheck/data/test/headwords.txt","r")
fconll = open(os_path+"articleCheck/data/test/data.conll","r")
func = open(os_path+"articleCheck/data/train/uncountable.txt","r")
fngram = open(os_path+"articleCheck/data/train/ngram.txt","r")
fresult = open(os_path+"articleCheck/data/test/result.txt","w")
fa = open(os_path+"articleCheck/data/train/a.txt","r")
fan = open(os_path+"articleCheck/data/train/an.txt","r")
fu = open(os_path+"articleCheck/data/train/conalpha.txt","r")
fnon = open(os_path+"articleCheck/data/train/nonarticle.txt","r")
fbody = open(os_path+"articleCheck/data/train/body.txt","r")
fphrase = open(os_path+"articleCheck/data/train/phrase.txt","r")
uc_words = []
a_words = []
an_words = []
con_alph = []
non_art = []
body = []
phrases = []
Dict_W = {'~':{5:0}}
Dict_WW = {'~':{'~':{5:0}}}
Dict_WH = {'~':{'~':{5:0}}}
Dict_WWW = {'~':{'~':{5:0}}}
Dict_Head = {'~':{5:0}}
Dict = {}
#uncountable
#some special example using a
#some special example using an
#consonant alphabet
for each in func.readlines():
    uc_words.append(each[:-1])
for each in fa.readlines():
    a_words.append(each[:-1])
for each in fan.readlines():
    an_words.append(each[:-1])
for each in fu.readlines():
    con_alph.append(each[:-1])
for each in fnon.readlines():
    non_art.append(each[:-1])
for each in fbody.readlines():
    body.append(each[:-1])
for each in fphrase.readlines():
    phrases.append(each[:-1])
PART = 0
for each in fngram.readlines():
    if each.find(' ')==-1:
        PART += 1
    else:
        pos1 = each.find(' ')
        pos2 = each[pos1+1:].find(' ')+pos1+1
        pos3 = each[pos2+1:].find(' ')+pos2+1
        pos4 = each[pos3+1:].find(' ')+pos3+1
        if PART==1:
            word = each[:pos1]
            if not (word in Dict_W):
                Dict_W[word]={}
                for k in range(4):
                    Dict_W[word][k] = 0
            Dict_W[word][0] = int(each[pos1+1:pos2])
            Dict_W[word][1] = int(each[pos2+1:pos3])
            Dict_W[word][2] = int(each[pos3+1:pos4])
            Dict_W[word][3] = int(each[pos4+1:])
        else:
            pos5 = each[pos4+1:].find(' ')+pos4+1
            word1 = each[:pos1]
            word2 = each[pos1+1:pos2]
            if PART==2:
                if not (word1 in Dict_WH):
                    Dict_WH[word1] = {}
                if not (word2 in Dict_WH[word1]):
                    Dict_WH[word1][word2] = {}
                    for k in range(4):
                        Dict_WH[word1][word2][k] = 0
                Dict_WH[word1][word2][0] = int(each[pos2+1:pos3])
                Dict_WH[word1][word2][1] = int(each[pos3+1:pos4])
                Dict_WH[word1][word2][2] = int(each[pos4+1:pos5])
                Dict_WH[word1][word2][3] = int(each[pos5+1:])
            else:
                if not (word1 in Dict_WW):
                    Dict_WW[word1] = {}
                if not (word2 in Dict_WW[word1]):
                    Dict_WW[word1][word2] = {}
                    for k in range(4):
                        Dict_WW[word1][word2][k] = 0
                Dict_WW[word1][word2][0] = int(each[pos2+1:pos3])
                Dict_WW[word1][word2][1] = int(each[pos3+1:pos4])
                Dict_WW[word1][word2][2] = int(each[pos4+1:pos5])
                Dict_WW[word1][word2][3] = int(each[pos5+1:])


sentence_ID = 0
Article = [([0]*5) for i in range(1000)]
value = [([0]*5) for i in range(1000)]
val = [0]*5
Ended = False
while True:
    line = fhead.readline()
    if len(line)==0:
        break
    if line.find(' ')==-1: #finish loading a sentence.
        if sentence_ID != 0:
            last = '#'
            posi = 0
            for each in words:
                print(each,end = ' ',file = fresult)
            for i in range(len(words)):
                if words[i]=='a' or words[i]=='an' or words[i]=='the':
                    continue
                if words[i][:-1].isdigit() and words[i][-1]=='s':
                    articleChoose(i,'the')
                    continue
                tmp = 0
                for j in range(4):
                    if (Article[i][j]>0):
                        tmp |= (1<<j)
                if tmp == 1: #only "a"
                    articleChoose(i,'a')
                    #print >>fresult, 'a',
                elif tmp == 2: #only "an"
                    #print >>fresult, 'an',
                    articleChoose(i,'an')
                elif tmp==4: #only "the"
                    #print >>fresult, 'the',
                    articleChoose(i,'the')
                elif tmp==8:
                    articleChoose(i,'')
                elif tmp!=8 and tmp!=0: #if not only "/"
                    #have too many choices
                    val[0] = val[1] = val[2] = val[3] = 0
                    val[0] += ORI_VALUE
                    val[1] += ORI_VALUE
                    if i>0:
                        #print >>fresult, owords[i-1],
                        if words[i-1] == 'a':
                            val[0] += ORI_VALUE
                        elif words[i-1] == 'an':
                            val[1] += ORI_VALUE
                        elif words[i-1] == 'the':
                            val[2] += ORI_VALUE
                        else:
                            val[3] += ORI_VALUE
                    if owords[i][0].isupper():
                        val[2] += 2*ORI_VALUE
                    for k in range(4):
                        val[k] += value[i][k]
                    #find the most probable result
                    choice = -1
                    MAX_VALUE = -1
                    choices_count = 0
                    for j in range(4):
                        if Article[i][j]>0:
                            choices_count += 1
                            if val[j]>MAX_VALUE:
                                MAX_VALUE = val[j]
                                choice = j
                    if choices_count!=1:
                        if i==0:
                            continue
                        if Article[i][0]!=0 or Article[i][1]!=0 or (words[i-1]!='an' and words[i-1]!='a'):
                            continue
                    if choice == 0:
                        #print >>fresult,'a',
                        articleChoose(i,'a')
                    elif choice == 1:
                        #print >>fresult,'an',
                        articleChoose(i,'an')
                    elif choice == 2:
                        #print >>fresult,'the',
                        articleChoose(i,'the')
                    else:
                        articleChoose(i,'')
                #print >>fresult, owords[i],
            total_len +=len(words)
        sentence_ID += 1
        words = []
        owords = []
        POS = []
        while True: #loading the conll
            each = fconll.readline()
            if len(each)==0:
                PrintError()
                Ended = True
                break
            if each[0]=='(':
                continue
            sets = each.split()
            if len(sets)==0:
                break
            words.append(sets[1].lower())
            owords.append(sets[1])
            POS.append(sets[3])
        for i in range(len(words)):
            for j in range(4):
                Article[i][j] = 0
                value[i][j] = 0
            #not really
            '''if (POS[i]=='JJS' or POS[i]=='RBS'):
                if (i<1 or (POS[i-1]!='POS' and POS[i-1]!='PDT' and POS[i-1]!='PRP' and POS[i-1]!='PRP$')):
                    Article[i][2] = 1 '''
        if Ended:
            break
    else:
        sets = line.split()
        pos = int(sets[0])-1
        begin = words[pos].lower()
        #articleChoose(pos,'the')
        if sets[0]==sets[1]: #only one word
            for k in range(4):
                if words[pos] in Dict_W:
                    value[pos][k] += Dict_W[words[pos]][k]*H_VALUE
                if pos>0:
                    if words[pos-1] in Dict_WH:
                        if words[pos] in Dict_WH[words[pos-1]]:
                            value[pos][k] += Dict_WH[words[pos-1]][words[pos]][k]*WH_VALUE
                    if words[pos-1] in Dict_WW:
                        if words[pos] in Dict_WW[words[pos-1]]:
                            value[pos][k] += Dict_WW[words[pos-1]][words[pos]][k]*WW_VALUE
            if Article[pos][0] or Article[pos][1] or Article[pos][2] or Article[pos][3]:
                continue
            if begin in non_art:
                Article[pos][0] = Article[pos][1] = Article[pos][2] = 0
                continue
            if begin=='breakfast' or begin=='lunch' or begin=='dinner' or begin=='supper':
                if pos>0:
                    lpos = pos-1
                    if words[lpos]=='the' or words[lpos]=='a' or words[lpos]=='an':
                        lpos -= 1
                    if lpos>=0:
                        if POS[lpos]=='VBP' or POS[lpos]=='VBZ' or POS[lpos]=='VBD' or POS[lpos]=='TO' or POS[lpos]=='IN':
                            Article[i][3]=1
                            continue
            if begin == 'most' or begin == 'much':
                Article[i][3] = 1
                continue
            #if it's the highest level e.g. He is 'the' tallest.
            if (POS[pos]=='JJS' or POS[pos]=='RBS' or POS[pos]=='JJ'):
                if (pos<1 or (POS[pos-1]!='POS' and POS[pos-1]!='PDT' and POS[pos-1]!='PRP' and POS[pos-1]!='PRP$')):
                    Article[pos][2] = 1
                    continue
            for j in range(4):
                Article[pos][j] = 1
            #if the headword isn't a noun (eg.I, me, her)
            if POS[pos]!='NN' and POS[pos]!='NNS' and POS[pos]!='NNP' and POS[pos]!='NNPS':
                Article[pos][0] = Article[pos][1] = Article[pos][2] = Article[pos][3] = 0
                continue
            checkAvsAn(pos, begin)
            #if the headword is uncoutable
            if begin in uc_words:
                Article[pos][0] = Article[pos][1] = 0
            #+s
            if POS[pos]=='NNS' or POS[pos]=='NNPS':
                Article[pos][0] = Article[pos][1] = 0
            if pos>1:
                if words[pos-1].lower()=='of' and (words[pos-2].lower()=='some' or words[pos-2].lower()=='most' or words[pos-2].lower()=='all' or words[pos-2].lower()=='one' \
                or words[pos-2].lower()=='any'):
                    Article[pos][0] = Article[pos][1] = Article[pos][3] = 0
            if pos>1:
                if words[pos-1].lower()=='by' and (words[pos] in body):
                    Article[pos][0] = Article[pos][1] = Article[pos][3] = 0
            #there be
            if pos>1:
                pos1 = pos - 1
                pos2 = pos - 2
                if checkTherebe(pos1,pos2) or checkTherebe(pos2,pos1):
                    Article[pos][2] = 0
                    continue
            #there * be
            if pos>2:
                pos1 = pos - 1
                pos2 = pos - 3
                if checkTherebe(pos1,pos2) or checkTherebe(pos2,pos1):
                    Article[pos][2] = 0
                    continue
            continue
        lpos = pos
        while begin=='a' or begin=='an' or begin=='the':
            pos += 1
            begin =words[pos].lower()
        posh = int(sets[2])-1
        head = words[ posh ].lower()
        len_of_phrase = int(sets[1])-int(sets[0])+1
        for k in range(4):
            if words[pos] in Dict_W:
                value[pos][k] += Dict_W[words[pos]][k]*H_VALUE
            if pos>0:
                if words[lpos-1] in Dict_WH:
                    if head in Dict_WH[words[lpos-1]]:
                        value[pos][k] += Dict_WH[words[lpos-1]][head][k]*WH_VALUE
                if words[lpos-1] in Dict_WW:
                    if words[pos] in Dict_WW[words[lpos-1]]:
                        value[pos][k] += Dict_WW[words[lpos-1]][words[pos]][k]*WW_VALUE
        if Article[pos][0] or Article[pos][1] or Article[pos][2] or Article[pos][3]:
            continue
        for j in range(4):
            Article[pos][j] = 1
        if len_of_phrase>=2:
            if (words[lpos]+' '+words[lpos+1]) in phrases:
                for i in range(4):
                    Article[pos][i] = 0
                if words[lpos]=='a':
                    Article[pos][0] = 1
                if words[lpos]=='an':
                    Article[pos][0] = 1
                if words[lpos]=='the':
                    Article[pos][0] = 1
                continue
        if (head in non_art) and POS[posh-1]!='JJ' and POS[posh-1]!='JJR' and POS[posh-1]!='JJS':
            Article[pos][0] = Article[pos][1] = Article[pos][2] = 0
            continue
        tmp = head[:-1]
        if tmp.isdigit() and head[-1]=='s':
            Article[pos][0] = Article[pos][1] = Article[pos][3] = 0
            continue
        #if begin=='my' or begin=='your' or begin=='his' or begin=='her' or begin=='our' or begin=='their':
        if POS[pos]=='POS' or POS[pos]=='PDT' or POS[pos]=='PRP' or POS[pos]=='PRP$' or begin=='many' or begin=='much':
            Article[pos][0] = Article[pos][1] = Article[pos][2] = 0
            continue
        #there has been a DT already
        if POS[pos]=='DT':
            Article[pos][0] = Article[pos][1] = Article[pos][2] = Article[pos][3] = 0
            continue
        #if it is the highest level and there isn't DT before
        if (POS[pos]=='JJS' or POS[pos]=='RBS'):
            if (begin!='most'):
                Article[pos][0] = Article[pos][1] = Article[pos][3] = 0
                continue
            else:
                if POS[pos+1]=='JJ':
                    Article[pos][0] = Article[pos][1] = Article[pos][3] = 0
                    continue
        if (head=='breakfast' or head=='lunch' or head=='dinner' or head=='supper'):
            poshb = posh - 1
            if words[poshb]=='the' or words[poshb]=='a' or words[poshb]=='an':
                poshb -= 1
            if poshb>=0:
                if POS[poshb]=='VBP' or POS[poshb]=='VBZ' or POS[poshb]=='VBD' or POS[poshb]=='TO' or POS[poshb]=='IN':
                    Article[pos][0]=Article[pos][1]=Article[pos][2]=0
                    continue
        #rank
        len_of_begin = len(begin)
        if (POS[pos]=='JJ') and len_of_begin>2:
            tmp = begin[:-2]
            last2 = begin[-2:]
            if (last2=='th' or last2=='st' or last2=='nd' or last2=='rd'):
                if tmp.isdigit():
                    Article[pos][0] = Article[pos][1] = Article[pos][3] = 0
                    continue
                elif last2=='th' or begin.find('first')==len_of_begin-5 or begin.find('second')==len_of_begin-6 or begin.find('third')==len_of_begin-5:
                    Article[pos][0] = Article[pos][1] = Article[pos][3] = 0
                    continue
        #some of, most of, all of, one of + 'the'
        if lpos>1:
            if words[lpos-1].lower()=='of' and (words[lpos-2].lower()=='some' or words[lpos-2].lower()=='most' or words[lpos-2].lower()=='all' or words[lpos-2].lower()=='one' \
            or words[lpos-2].lower()=='any'):
                Article[pos][0] = Article[pos][1] = Article[pos][3] = 0
            if words[lpos-1].lower()=='by' and (words[int(set[3])-1] in body):
                Article[pos][0] = Article[pos][1] = Article[pos][3] = 0
        checkAvsAn(pos,begin)
        #if head is uncountable
        if head in uc_words:
            Article[pos][0] = Article[pos][1] = 0
        #+s
        if POS[posh]=='NNS' or POS[posh]=='NNPS':
            Article[pos][0] = Article[pos][1] = 0
        if Article[pos][0] + Article[pos][1] + Article[pos][2] + Article[pos][3] < 2:
            continue
        #there be
        if lpos>1:
            pos1 = lpos - 1
            pos2 = lpos - 2
            if checkTherebe(pos1,pos2) or checkTherebe(pos2,pos1):
                Article[pos][2] = 0
                continue
        #there * be
        if lpos>2:
            pos1 = lpos - 1
            pos2 = lpos - 3
            if checkTherebe(pos1,pos2) or checkTherebe(pos2,pos1):
                Article[pos][2] = 0
                continue
        if Article[pos][0] + Article[pos][1] + Article[pos][2] + Article[pos][3] < 2:
            continue
        if head in Dict:
            value[pos][2] += P_VALUE
ftext.close()
fhead.close()
fconll.close()
func.close()
fngram.close()
fresult.close()
fa.close()
fan.close()
fu.close()
fnon.close()
