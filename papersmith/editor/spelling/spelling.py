# -*- coding: utf-8 -*-
import re
from papersmith.editor.issue import Issue
from papersmith.editor.spelling.correction import edit_distance

def check(content):
    proper_noun=eval(open("papersmith/editor/spelling/proper_nouns.txt").read())
    issues=[]
    pos=0
    w=''
    for i in content:
        if (ord(i)>64 and ord(i)<91) or (ord(i)>96 and ord(i)<123) or ord(i)== 39:
            w+=i
            if len(w)==1 and w=='\'':
                pos+=1
                w=''
            continue
        if len(w)==0:
            pos+=1
            continue
        if w in proper_noun:
            if ord(w[0])>96 and ord(w[0])<123:
                issue = Issue(1, 1, [pos], [pos+len(w)], chr(ord(w[0])-32)+w[1:].lower(), 0)
                issues.append(issue)
        elif not (w.isupper() or w.istitle()):
            s=w.lower()
            word=edit_distance(s)
            if word != s :
                issue = Issue(1, 1, [pos], [pos+len(w)], word, 0)
                issues.append(issue)
        pos+=len(w)+1
        w=''
    return issues
