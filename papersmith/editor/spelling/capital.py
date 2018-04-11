# -*- coding: utf-8 -*-

from papersmith.editor.issue import Issue

def check(content):
    s=eval(open("papersmith/editor/spelling/say.txt").read())
    issues = []
    for j in range(5):
        if content[j]=='\'' or content[j]=='\"' or content[j]==' ':
            continue
        if ord(content[j])>96 and ord(content[j])<123:
            l=0
            for k in range(100):
                if (ord(content[j+k+1])>96 and ord(content[j+k+1])<123) or (ord(content[j+k+1])>64 and ord(content[j+k+1])<91) or ord(content[j+k+1])=="'":
                    l+=1
                else:
                    break
            string=chr(ord(content[j])-32)
            for k in range(l):
                string+=content[j+k+1]
            issues.append(Issue(1,1,[j],[j+l+1],string,0))
            break
        break
    yinhao_num=0
    if content[0]=="'" or content[0]=='\"':
        yinhao_num+=1
    for i in range(1,len(content)):
        if content[i] =='!' or content[i] =='?' or (content[i] =='.'and not content[i-1].isupper()):
            huanhang=0
            yinhao=0
            for j in range(10):
                if i+j+1>=len(content):
                    break
                if content[i+j+1]==' ':
                    continue
                if content[i+j+1]=='\n':
                    huanhang=1
                    continue
                if content[i+j+1]=='\'' or content[i+j+1]=='\"':
                    yinhao=1
                    yinhao_num+=1
                    continue
                if ord(content[i+j+1])>96 and ord(content[i+j+1])<123:
                    w=''
                    ww=''
                    for k in range(100):
                        w+=content[i+j+k+1]
                        if not((ord(content[i+j+k+2])>96 and ord(content[i+j+k+2])<123) or (ord(content[i+j+k+2])>64 and ord(content[i+j+k+2])<91) or content[i+j+k+2]=="'"):
                            break
                    for k in range(30):
                        if (ord(content[i+j+k+len(w)+2])>96 and ord(content[i+j+k+len(w)+2])<123):
                            ww+=content[i+j+k+len(w)+2]
                        else:
                            break
                    if yinhao==0 or huanhang==1 or yinhao_num%2==1 or not ( w in s or ww in s):
                        string=chr(ord(content[i+j+1])-32)
                        for k in range(len(w)-1):
                            string+=content[i+j+k+2]
                        issues.append(Issue(1,1,[i+j+1],[i+j+len(w)+1],string,0))
                    break
                break
    return issues # List of issues
