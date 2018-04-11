f = open("output.txt","r")
os_path = "papersmith/editor/grammar/articleCheck/"
fout = open(os_path+"data/test/output.txt","w")
for each in f.readlines():
    print(each, end = ' ')
    print(each,end = ' ', file = fout)
