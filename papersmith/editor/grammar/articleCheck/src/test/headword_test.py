os_path = "papersmith/editor/grammar/"
fphrase = open(os_path+"articleCheck/data/test/NP.txt","r")
fconll = open(os_path+"articleCheck/data/test/data.conll","r")
fhead = open(os_path+"articleCheck/data/test/headwords.txt","w")
sentence_ID = 0
words = []
POS = []
'''father = []
link = []'''
G = [[0 for i in range(500)] for i in range(500)]
for line in fphrase.readlines():
    line = line.strip()
    if len(line)==0:
        continue
    if line.find(' ')!=-1:
        Num = line.split()
        begin = int(Num[0])
        end = int(Num[1])
        head = 0
        if begin == end:
            head = begin
        else:
            for i in range(begin,end+1):
                for j in range(len(words)+1):
                    if G[j][i]!=0:
                        if j<begin or j>end:
                            if i>head:
                                head = i
        '''nhead = 0
        if begin == end:
            head = begin
        else:
            for i in range(begin,end+1):
                print sentence_ID
                if father[i-1]<begin or father[i-1]>end:
                    if POS[i-1][0]=='N':
                        if i>head:
                            head = i
                    if i>nhead:
                        nhead = i
        if head==0:
            head = nhead'''
        print(begin, end, head,file = fhead)
    else:
        sentence_ID += 1
        print(sentence_ID, file = fhead)
        word = fconll.readline()
        words = []
        POS = []
        G = [[0 for i in range(500)] for i in range(500)]
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
            else:
                pos = word.find(',')
                ID1 = int(word[1:pos])
                ID2 = int(word[pos+2:-2])
                G[ID1][ID2] = 1
            '''father.append(int(sets[5]))
            link.append(sets[6])'''
            word = fconll.readline()
        #if sentence_ID == 175:
print(sentence_ID+1, file = fhead)
fphrase.close()
fconll.close()
fhead.close()
