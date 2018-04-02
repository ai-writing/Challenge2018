class node:
    def __init__(self):
        self.sons=[-1]*28

nodelist=[node()]

def gen_trie():
	global nodelist
	nodenum=1
	currentnode=0
	t = eval(open("papersmith/editor/spelling/frequency.txt").read())
	for key,value in t.items():
		for i in key:
			if i=='\'':
				if nodelist[currentnode].sons[26] < 0:
				    nodelist.append(node())
				    nodelist[currentnode].sons[26] = nodenum
				    nodenum += 1
				currentnode = nodelist[currentnode].sons[26]
			else:
				if nodelist[currentnode].sons[ord(i)-97]<0:
				    nodelist.append(node())
				    nodelist[currentnode].sons[ord(i) - 97] = nodenum
				    nodenum += 1
				currentnode=nodelist[currentnode].sons[ord(i)-97]
		nodelist[currentnode].sons[27]=value
		currentnode=0

def edit_distances(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz\''
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)
def edit_distance1(word):
    wordlist=[]
    s=edit_distances(word)
    for i in s:
        if wordfrequency(i)>0:
            wordlist.append(i)
    if len(wordlist)>0:
        return sorted(wordlist,key=lambda x:-wordfrequency(x))[0]
    return ''
def edit_distance2(word):
    wordlist=[]
    s=edit_distances(word)
    for i in s:
        ss=edit_distances(i)
        for j in ss:
            if j not in wordlist and wordfrequency(j)>0:
                wordlist.append(j)
    if len(wordlist)>0:
        return sorted(wordlist,key=lambda x:-wordfrequency(x))[0]
    return ''
def wordfrequency(word):
    global nodelist
    currentnode=0
    for i in word:
        if i=='\'':
            if nodelist[currentnode].sons[26] < 0:
                return -1
            currentnode=nodelist[currentnode].sons[26]
        else:
            if nodelist[currentnode].sons[ord(i)-97]<0:
                return -1
            currentnode=nodelist[currentnode].sons[ord(i)-97]
    return nodelist[currentnode].sons[27]
def edit_distance(word): 
    global nodelist
    keyboard={'q':['w','a'],'w':['q','a','s','e'],
              'e':['w','s','d','r'],'r':['e','d','f','t'],
              't':['r','f','g','y'],'y':['t','g','h','u'],
              'u':['y','h','j','i'],'i':['u','j','k','o'],
              'o':['i','k','l','p'],'p':['o','l'],
              'a':['w','q','s','z'],'s':['w','a','e','d','x','z'],
              'd':['e','r','f','c','x','s'],'f':['r','t','g','v','c','d'],
              'g':['t','y','h','b','v','f'],'h':['y','u','j','n','b','g'],
              'j':['u','i','k','m','n','h'],'k':['i','o','l','m','j'],
              'l':['k','o','p'],'z':['s','a','x'],
              'x':['z','s','d','c'],'c':['x','d','f','v'],
              'v':['c','f','g','b'],'b':['v','g','h','n'],
              'n':['b','h','j','m'],'m':['n','j','k']}
    
    if wordfrequency(word)>0:
        return word
    for i in range(len(word)):
        w=word[:i]+'\''+word[i:]
        if wordfrequency(w)>0:
            return w
    l=[]
    for i in range(len(word)):
        if word[i] != '\'':
            for j in keyboard[word[i]]:
                l.append(word[:i]+j+word[i+1:])
    wordlist=[]
    kbword=''
    for i in l:
        if wordfrequency(i)>0:
            wordlist.append(i)
    if len(wordlist)>0:
        kbword=sorted(wordlist,key=lambda x:-wordfrequency(x))[0]
    word1=edit_distance1(word)
    if len(word1)>0:
        if len(kbword)>0:
            if wordfrequency(word1)>=wordfrequency(kbword)*10:
                return word1
            else:
                return kbword
        else:
            return word1
    else:
        if len(kbword)>0:
            return kbword
    if len(word)>7:
        return edit_distance2(word)
    return ' '
