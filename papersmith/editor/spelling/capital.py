# -*- coding: utf-8 -*-

from papersmith.editor.issue import Issue

def check(content):
    issues = []
    for j in range(5):
        if content[j]=='\'' or content[j]=='\"' or content[j]==' ':
            continue
        if ord(content[j])>96 and ord(content[j])<123:
            issues.append(Issue(1,1,[j],[j+1],chr(ord(content[j])-32),0))
            break
        break
    for i in range(len(content)):
        if content[i] =='!' or content[i] =='?' or content[i] =='.':
            for j in range(5):
                if i+j+1>=len(content):
                    break
                if content[i+j+1]=='\'' or content[i+j+1]=='\"' or content[i+j+1]==' ':
                    continue
                if ord(content[i+j+1])>96 and ord(content[i+j+1])<123:
                    issues.append(Issue(1,1,[i+j+1],[i+j+2],chr(ord(content[i+j+1])-32),0))
                    break
                break
    
    return issues # List of issues
