fdata = open("../data/data.txt","r")
ftext = open("../data/text.txt","w")
words = []
for each in fdata.readlines():
    each = each[:-1]
    while len(each)>0:
        pos1 = each.find('.')
        if pos1 == -1:
            pos1 = 1<<30
        pos2 = each.find('?')
        if pos2 == -1:
            pos2 = 1<<30
        pos3 = each.find('!')
        if pos3 == -1:
            pos3 = 1<<30
        pos = min(pos1,pos2)
        pos = min(pos,pos3)
        if pos == 1<<30:
            pos = -1
        #pos = min(pos, each.find('!'))
        st1 = each[:pos]
        words1 = st1.split()
        words += words1
        for word in words:
            print >>ftext, word,
        print >>ftext,each[pos]
        print each[pos]
        words = []
        if pos == -1:
            each = ''
        else:
            each = each[pos+1:]
