#null, a, an, the
Dict_W = {'~':{'~':0}}
Dict_WW = {'~':{'~':{'~':0}}}
Dict_WH = {'~':{'~':{'~':0}}}
Dict_WWW = {'~':{'~':{'~':0}}}
Dict_Head = {'~':{'~':0}}
Fset = [10, 10, 5, 3]
Wset = [0, 10, 10, 10]
fconll = open("../../data/train/data.conll","r")
fhead = open("../../data/train/headwords.txt","r")
fngram = open("../../data/train/ngram.txt","w")
sentence_ID = 0
words = []
POS = []
'''father = []
link = []'''
for line in fhead.readlines():
    if len(line)==0:
        continue
    if line.find(' ')!=-1:
        Num = line.split()
        begin = int(Num[0])
        end = int(Num[1])
        head = int(Num[2])
        begin -= 1
        end -= 1
        head -= 1
        if not Dict_Head.has_key(words[head]):
            Dict_Head[words[head]] = {}
            Dict_Head[words[head]]['a'] = 0
            Dict_Head[words[head]]['an'] = 0
            Dict_Head[words[head]]['the'] = 0
            Dict_Head[words[head]][' '] = 0
        if words[begin]=='an':
            Dict_Head[words[head]]['an'] += 1
        elif words[begin]=='a':
            Dict_Head[words[head]]['a'] += 1
        elif words[begin]=='the':
            Dict_Head[words[head]]['the'] += 1
        else:
            Dict_Head[words[head]][' '] += 1
        if begin>0:
            if not Dict_WH.has_key(words[head]):
                Dict_WH[words[head]] = {}
            if not Dict_WH[words[head]].has_key(words[begin-1]):
                Dict_WH[words[head]][words[begin-1]] = {}
                Dict_WH[words[head]][words[begin-1]]['a'] = 0
                Dict_WH[words[head]][words[begin-1]]['an'] = 0
                Dict_WH[words[head]][words[begin-1]]['the'] = 0
                Dict_WH[words[head]][words[begin-1]][' '] = 0
                if words[begin]=='an':
                    Dict_WH[words[head]][words[begin-1]]['an'] += 1
                elif words[begin]=='a':
                    Dict_WH[words[head]][words[begin-1]]['a'] += 1
                elif words[begin]=='the':
                    Dict_WH[words[head]][words[begin-1]]['the'] += 1
                else:
                    Dict_WH[words[head]][words[begin-1]][' '] += 1
            nbegin = begin
            if words[nbegin]=='a' or words[nbegin]=='an' or words[nbegin]=='the':
                nbegin += 1
            if nbegin>end:
                continue
            if not Dict_WW.has_key(words[nbegin]):
                Dict_WW[words[nbegin]] = {}
            if not Dict_WW[words[nbegin]].has_key(words[begin-1]):
                Dict_WW[words[nbegin]][words[begin-1]] = {}
                Dict_WW[words[nbegin]][words[begin-1]]['a'] = 0
                Dict_WW[words[nbegin]][words[begin-1]]['an'] = 0
                Dict_WW[words[nbegin]][words[begin-1]]['the'] = 0
                Dict_WW[words[nbegin]][words[begin-1]][' '] = 0
                if words[begin]=='an':
                    Dict_WW[words[nbegin]][words[begin-1]]['an'] += 1
                elif words[begin]=='a':
                    Dict_WW[words[nbegin]][words[begin-1]]['a'] += 1
                elif words[begin]=='the':
                    Dict_WW[words[nbegin]][words[begin-1]]['the'] += 1
                else:
                    Dict_WW[words[nbegin]][words[begin-1]][' '] += 1

    else:
        sentence_ID += 1
        word = fconll.readline()
        words = []
        POS = []
        '''father = []
        link = []'''
        while len(word)>0:
            if word[0]!='(':
                sets = word.split()
                if len(sets)==0:
                    break
                sets[1] = sets[1].lower()
                words.append(sets[1])
                POS.append(sets[3])
                '''father.append(int(sets[5]))
                link.append(sets[6])'''
            word = fconll.readline()
        print sentence_ID
        print words
print >>fngram,1
for each in Dict_Head:
    if each!='~':
        print >>fngram, each, Dict_Head[each][' '], Dict_Head[each]['a'], Dict_Head[each]['an'], Dict_Head[each]['the']
print >>fngram,2
for eachH in Dict_WH:
    if eachH!='~':
        for eachW in Dict_WH[eachH]:
            print >>fngram, eachW, eachH, Dict_WH[eachH][eachW][' '], Dict_WH[eachH][eachW]['a'], Dict_WH[eachH][eachW]['an'], Dict_WH[eachH][eachW]['the']
print >>fngram,3
for eachW2 in Dict_WW:
    if eachW2!='~':
        for eachW1 in Dict_WW[eachW2]:
            print >>fngram, eachW1, eachW2, Dict_WW[eachW2][eachW1][' '], Dict_WW[eachW2][eachW1]['a'], Dict_WW[eachW2][eachW1]['an'], Dict_WW[eachW2][eachW1]['the']
