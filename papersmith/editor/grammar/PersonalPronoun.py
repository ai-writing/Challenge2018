# -*- coding: utf-8 -*-

from papersmith.editor.issue import Issue

def check(content):
    '检查内容中的语法错误'
    PRPlist=[['I','me','my','mine'],['you','you','your','yours'],['he','him','his','his'],['she','her','her','hers'],['we','us','our','ours'],['they','them','their','theirs'],['it','it','its','its']]
    preposition=eval(open('papersmith/editor/grammar/preposition.txt').read())
    issues=[]
    pos=0
    w=''
    for i in range(len(content)):
        if (ord(content[i])>64 and ord(content[i])<91) or (ord(content[i])>96 and ord(content[i])<123) :
            w+=content[i]
            continue
        if len(w)==0:
            pos+=1
            continue
        if w.lower() in preposition:
            for j in range(100):
                if i+j+1>=len(content):
                    break
                if content[i+j+1]==' ':
                    continue
                if ord(content[i+j+1])>96 and ord(content[i+j+1])<123:
                    p=''
                    for k in range(100):
                        p+=content[i+j+k+1]
                        if not(ord(content[i+j+k+2])>96 and ord(content[i+j+k+2])<123):
                            break
                    for k in PRPlist:
                        if p!=k[1] and p ==k[0]:
                            issues.append(Issue(2,1,[i+j+1],[i+j+len(p)+1],k[1],0))
                break
        w=''
            
    return issues # List of issues
