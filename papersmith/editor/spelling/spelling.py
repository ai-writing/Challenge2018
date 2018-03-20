# -*- coding: utf-8 -*-
import re
from papersmith.editor.issue import Issue
from papersmith.editor.spelling.correction import edit_distance

def check(content):
    issues=[]
    pos=0
    w=''
    for i in content:
        if (ord(i)>64 and ord(i)<91) or (ord(i)>96 and ord(i)<123):
            w+=i
            continue
        if len(w)==0:
            pos+=1
            continue
        if not (w.isupper() or w.istitle()):
            s=w.lower()
            word=edit_distance(s)
            if word != s :
                issue = Issue(1, 1, [pos], [pos+len(w)], word, 0)
                issues.append(issue)
        pos+=len(w)+1
        w=''
    return issues
