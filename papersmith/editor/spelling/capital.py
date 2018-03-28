# -*- coding: utf-8 -*-

from papersmith.editor.issue import Issue

def check(content):
    issues = []
    for j in range(5):
        if content[j]=='\'' or content[j]=='\"' or content[j]==' ':
            continue
        if ord(content[j])>96 and ord(content[j])<123:
            l=0
            for k in range(100):
                if (ord(content[j+k+1])>96 and ord(content[j+k+1])<123) or (ord(content[j+k+1])>64 and ord(content[j+k+1])<91):
                    l+=1
                else:
                    break
            string=chr(ord(content[j])-32)
            for k in range(l):
                string+=content[j+k+1]
            issues.append(Issue(1,1,[j],[j+l+1],string,0))
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
                    l=0
                    for k in range(100):
                        if (ord(content[i+j+k+2])>96 and ord(content[i+j+k+2])<123) or (ord(content[i+j+k+2])>64 and ord(content[i+j+k+2])<91):
                            l+=1
                        else:
                            break
                    string=chr(ord(content[i+j+1])-32)
                    for k in range(l):
                        string+=content[i+j+k+2]
                    issues.append(Issue(1,1,[i+j+1],[i+j+l+2],string,0))
                    break
                break
    
    return issues # List of issues
