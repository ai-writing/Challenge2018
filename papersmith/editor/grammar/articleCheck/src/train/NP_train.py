def get_num(line, i):
    s = 0
    while line[i].isdigit():
        s = s * 10 + int(line[i])
        i = i + 1
    return s

ftree = open("../../data/train/tree.txt","r")
fphrase = open("../../data/train/NP.txt","w")
sentence_ID = 0
for line in ftree.readlines():
    sentence_ID += 1
    print >>fphrase, sentence_ID
    for i in range(len(line)):
        if line[i]=='N' and line[i+1]=='P' and line[i-1]=='(' and line[i+2]=='(':
            index_pre = i
            while not line[index_pre].isdigit():
                #print index_pre
                index_pre += 1
            begin = get_num(line,index_pre)
            end = begin
            index_next = i+2
            Top = 0
            while True:
                if line[index_next]==' ':
                    continue
                if line[index_next]=='(':
                    Top += 1
                if line[index_next]==')':
                    Top -= 1
                if Top<0:
                    break
                if line[index_next].isdigit() and not line[index_next-1].isdigit():
                    end = get_num(line,index_next)
                index_next += 1
            print >>fphrase, begin, end
