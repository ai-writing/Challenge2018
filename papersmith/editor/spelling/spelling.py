# -*- coding: utf-8 -*-

from papersmith.editor.issue import Issue
from papersmith.editor.spelling.correction import edit_distance

def check(content):
    issues=[]
    pos=0
    words=content.split()
    for i in words:
        word=edit_distance(i)
        if word != i :
           issue = Issue(1, 1, pos, pos+len(i)-1, word, 0)
           issues.append(issue)
        pos+=len(i)+1
    return issues
