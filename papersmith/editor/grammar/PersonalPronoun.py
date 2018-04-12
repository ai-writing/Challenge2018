# -*- coding: utf-8 -*-

from papersmith.editor.issue import Issue

def check(content):
    '检查内容中的语法错误'
    PRPlist=[['I','me','my','mine'],['you','you','your','yours'],['he','him','his','his'],['she','her','her','hers'],['we','us','our','ours'],['they','them','their','theirs'],['it','it','its','its']]
    preposition=eval(open('preposition.txt').read())
    issues=[]
    pos=0
    w=''
    for i in content:
        if (ord(i)>64 and ord(i)<91) or (ord(i)>96 and ord(i)<123) :
            w+=i
            continue
        if len(w)==0:
            pos+=1
            continue
        if w in preposition:
            for 
            
    return issues # List of issues
