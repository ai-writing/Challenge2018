import os


def articleCheck(content):
    #print content
    os_path = "papersmith/editor/grammar/articleCheck/"
    fout = open("output.txt","w")
    fout.close()
    f = open(os_path+"data/text.txt","w")
    print(content,file = f)
    f.close()
    os.system("java -jar "+os_path+"src/Parser.jar "+os_path+"data/text.txt")
    os.system("python "+os_path+"src/copyoutput.py")
    os.system("python "+os_path+"src/test/phrase_test.py")
    os.system("python "+os_path+"src/test/NP_test.py")
    os.system("python "+os_path+"src/test/headword_test.py")
    os.system("python "+os_path+"src/test/test.py")#
    fresult = open(os_path+"data/test/result.txt","r")
    fsets = open(os_path+"data/test/sets.txt","w")
    sentence = fresult.readline()
    print(sentence, file = fsets)
    words = sentence.split()
    lcontent = content.lower()
    begin = 0
    posi = []
    for each in words:
        tmp = lcontent.find(each,begin)
        posi.append(tmp)
        if each!='-lrb-' and each!='-rrb-':
            begin = tmp + len(each)
    print(content, file = fsets)
    print(words, file = fsets)
    print(posi, file = fsets)
    Issues = []
    for line in fresult.readlines():
        pos1 = line.find(' ')
        le = int(line[:pos1])
        pos2 = line[pos1+1:].find(' ') + pos1+1
        ri = int(line[pos1+1:pos2])
        str = line[pos2+1:-1]
        #print((posi[le],posi[ri+1]-1,str), file = fsets)
        posir=posi[ri+1]
        while lcontent[posir-1]==' ':
            posir -= 1
        Issue = (posi[le], posir, str)
        Issues.append(Issue)
    fresult.close()
    print(Issues, file= fsets)
    return Issues
    return []
