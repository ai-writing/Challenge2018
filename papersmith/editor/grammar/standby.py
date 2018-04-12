w=open('a.txt').readlines()
l=[]
for i in w:
    l.append(i.split()[0])
f=open('preposition.txt','w')
f.write(str(l))
