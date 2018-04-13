# -*- coding: utf-8 -*-

from papersmith.editor.issue import Issue

def check(content):
    PRPlist=[['I','me','my','mine'],['you','you','your','yours'],['he','him','his','his'],['she','her','her','hers'],['we','us','our','ours'],['they','them','their','theirs'],['it','it','its','its']]
    preposition=eval(open('papersmith/editor/grammar/preposition.txt').read())
    issues=[]
    w=''
    for i in range(len(content)):
        if (ord(content[i])>64 and ord(content[i])<91) or (ord(content[i])>96 and ord(content[i])<123) or content[i]=="'":
            w+=content[i]
            if len(w)==1 and w=='\'':
                w=''
            continue
        if len(w)==0:
            continue
        if w.lower() in preposition:
            for j in range(100):
                if i+j+1>=len(content):
                    break
                if content[i+j+1]==' ':
                    continue
                if (ord(content[i+j+1])>96 and ord(content[i+j+1])<123) or (ord(content[i+j+1])>64 and ord(content[i+j+1])<91):
                    p=''
                    for k in range(100):
                        p+=content[i+j+k+1]
                        if not((ord(content[i+j+k+2])>96 and ord(content[i+j+k+2])<123) or (ord(content[i+j+k+2])>64 and ord(content[i+j+k+2])<91) or content[i+j+k+2]=="'"):
                            break
                    for k in PRPlist:
                        if p in k:       
                            if p==k[0] and p !=k[1]:
                                issues.append(Issue(1, 1, [i+j+1], [i+j+1+len(p)], k[1], 0))
                            elif p==k[2] and p!=k[3] and (content[i+j+1+len(p)] in ['.','!','?'] or content[i+j+2+len(p)] in ['.','!','?'] or content[i+j+3+len(p)] in ['.','!','?']):
                                issues.append(Issue(1, 1, [i+j+1], [i+j+1+len(p)], k[3], 0))
                            break
                break
        w=''
            
    return issues # List of issues
