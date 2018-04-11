
os_path = "papersmith/editor/grammar/"
f = open(os_path+"articleCheck/data/test/output.txt","r")
ftext = open(os_path+"articleCheck/data/test/text.txt","r")
ftree = open(os_path+"articleCheck/data/test/tree.txt","w")
fconll = open(os_path+"articleCheck/data/test/data.conll","w")
tree = ""
ntree = ""
First = True
ID = 0
Words = []
words_lower = []
POS = []
father = []
link = []
edge = []
'''ID_stack = []
pos_stack = []'''
sentence_ID = 0
for line in f.readlines():
    line=line.strip()
    if len(line)==0:
        continue
    if line=='(ROOT' and not First:
        sentence_ID += 1
        '''sentence = ftext.readline()
        words = sentence.split()
        while len(words)==0:
            sentence = ftext.readline()
            words = sentence.split()'''
        print(tree, file = ftree)
        #print >>ftree,sentence_ID,ntree
        #print >>ftree,sentence_ID,
        #print sentence
        while len(father)<len(Words):
            father.append(0)
            link.append("punct")
        Root = 0
        for i in range(len(Words)):
            if link[i]=='root':
                Root = i+1
        for i in range(len(Words)):
            if i+1!=Root and father[i]==0:
                father[i] = Root
        for i in range(len(Words)):
            print(i+1, Words[i], words_lower[i], POS[i], '-', file = fconll)
            #, father[i], link[i]
        for each in edge:
            print(each, file = fconll)
        print(file = fconll)
        Words = []
        words_lower = []
        POS = []
        father = []
        link = []
        '''pos_stack = []
        ID_stack = []'''
        edge = []
        tree = ''
        ntree = ''
        ID = 0
    new_line = ''
    i = 0
    if line[0]!='(':
        pos_l = line.find('(')
        pos_r = line.find(')')
        while not line[pos_r-1].isdigit():
            pos_r -= 1
        pos_c = line.find(',')
        pos1 = line.find('-',pos_l,pos_c)
        while line.find('-',pos1+1,pos_c)!=-1:
            pos1 = line.find('-',pos1+1,pos_c)
        pos2 = line.find('-',pos_c)
        while line.find('-',pos2+1)!=-1:
            pos2 = line.find('-',pos2+1)
        now_ID = int(line[pos2+1:pos_r])
        while not line[pos_c-1].isdigit():
            pos_c -= 1
        father_ID = int(line[pos1+1:pos_c])
        edge.append((father_ID, now_ID))
        '''if now_ID<len(father)+1:
            continue
        while now_ID!=len(father)+1:
            father.append(0)
            link.append('punct')'''
        '''father.append(int(line[pos1+1:pos_c]))
        link.append(line[:pos_l])'''
        continue
    '''pos_stack.append(-1)
    ID_stack.append(0)'''
    while i<len(line):
        '''if line[i]=='(':
            pos_stack.append(i)
            ID_stack.append(-1)
        if line[i]==')':
            while True:
                tmp = ID_stack[-1]
                ID_stack.pop()
                pos_stack.pop()
                if tmp == -1:
                    break'''
        if line[i]==' ' and line[i+1]!='(':
            j = i+1
            while line[j]!=')':
                j = j + 1
            ID = ID + 1
            Words.append(line[i+1:j])
            words_lower.append(line[i+1:j].lower())
            pos = ''
            while line[i-1]!='(':
                pos = line[i-1]+pos
                i -= 1
            POS.append(pos)
            new_line += "("+str(ID)+")"
            '''ID_stack.pop()
            pos_stack.pop()
            tmp = len(ID_stack)-1
            while ID_stack[tmp]==-1:
                tmp -= 1
            pos_stack.append(i+1)
            ID_stack.append(ID)
            pos_stack.append(i+1)
            ID_stack.append(-1)
            father.append(ID_stack[tmp])
            link.append("punkt")'''
            i = j-1
        elif line[i]!=' ':
            new_line +=line[i]
        i = i + 1
    if line[0]=='(':
        ntree+=line
    line=new_line
    if line[0]=='(':
        tree+=line
    First = False
print(tree, file = ftree)
while len(father)<len(Words):
    father.append(0)
    link.append("punct")
Root = 0
for i in range(len(Words)):
    if link[i]=='root':
        Root = i+1
for i in range(len(Words)):
    if i+1!=Root and father[i]==0:
        father[i] = Root
for i in range(len(Words)):
    print(i+1, Words[i], words_lower[i], POS[i], '-', father[i], link[i], file = fconll)
for each in edge:
    print(each, file = fconll)
print(file = fconll)
f.close()
ftext.close()
ftree.close()
fconll.close()
