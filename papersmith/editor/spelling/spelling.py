# -*- coding: utf-8 -*-
import re
from papersmith.editor.issue import Issue
from papersmith.editor.spelling.correction import edit_distance

def check(content):
    proper_noun=eval(open("papersmith/editor/spelling/proper_nouns.txt").read())
    irregular_plurals=eval(open('papersmith/editor/spelling/irregular_plurals.txt').read())
    uncountable_nouns=eval(open('papersmith/editor/spelling/uncountable_nouns.txt').read())
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
        extra_len=0
        if w[-1]=='\'':
            w=w[:-1]
            extra_len=1
        elif w[-2:]=="'s":
            w=w[:-2]
            extra_len=2
        if w.lower() in uncountable_nouns:
            if ord(w[0])>96 and ord(w[0])<123:
                issues.append(Issue(1, 1, [pos], [pos+len(w)], uncountable_nouns[w.lower()], 0))
            else:
                issues.append(Issue(1, 1, [pos], [pos+len(w)], uncountable_nouns[w.lower()].title(), 0))
        elif w.lower() in irregular_plurals:
            if ord(w[0])>96 and ord(w[0])<123 and w!='chineses' and w!='japaneses' and w!='swisses'and w!='germen'and w!='frenchmans' and w!='englishmans':
                issues.append(Issue(1, 1, [pos], [pos+len(w)], irregular_plurals[w.lower()], 0))
            else:
                issues.append(Issue(1, 1, [pos], [pos+len(w)], irregular_plurals[w.lower()].title(), 0))
        elif w in proper_noun:
            if ord(w[0])>96 and ord(w[0])<123:
                issues.append(Issue(1, 1, [pos], [pos+len(w)], chr(ord(w[0])-32)+w[1:].lower(), 0))
        elif not (w.isupper() or w.istitle()):
            s=w.lower()
            word=edit_distance(s)
            if word != s :
                issues.append(Issue(1, 1, [pos], [pos+len(w)], word, 0))
        pos+=len(w)+1+extra_len
        w=''
    return issues
