# -*- coding: utf-8 -*-
import re
from papersmith.editor.issue import Issue
from papersmith.editor.spelling.correction import edit_distance

def check(content):
    issues=[]
    pos=0
    words=re.split(r'[1234567890;,\s.!?\"<>\-:\\()+=|{}[\]@#$%^&*]\s*',content)
    for i in words:
        if len(i)>0:
            if not (i.isupper() or i.istitle()):
                w=i.lower()
                word=edit_distance(w)
                if word != w :
                   issue = Issue(1, 1, [pos], [pos+len(i)], word, 0)
                   issues.append(issue)
        pos+=len(i)+1
    return issues
