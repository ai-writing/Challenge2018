#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'single three'

__author__='Jay Gao 1219'

import nltk
import nltk.data

scentence="""
Yesterday a beggar knocked at my door. 
"""


Big_table=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
Small_table=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

g1=r"""
N:{<NN|NNS|NNP|NNPS|CD>}
NP: {<DT|PP\$>?<JJ|CD|PRP>*<N|PRP><N>?<INP>?}
NP:{<NP><CC><NP>}
NP:{<NP><IN><NP>}
NP:{<NP><NP>+}
V:{<VBD|VBN|VBP>?<VB|VBD|VBG|VBN|VBP|BNZ|VBZ>}
TV:{<TO><V>}
VP:{<V><NP>}
IN:{<JJR>?<IN>}
INP:{<IN><NP>}
VNP:{<IN><VP|V>}
INN:{<JJR><IN>}
ROOT:{<INP>?<NP><VP|V><INP>?}
{<NP|PRP><VP|V><IIN><NP><INN>?}

"""

groups=[['are','is'],['am','is'],['have','has'],['were','was']]

def word_callout(string):
    string=nltk.word_tokenize(string)
    string=nltk.pos_tag(string)
    return string

def if_single_n(np):
    l=len(np)
    l=list(range(l))
    l.reverse()
    for i in l:
        if type(np[i])==tuple:#只有一种可能，PRP
            if np[i][0] in ['he','He','she','She','it','It']:
                return True;
            else:
                return False;
            pass;
        else:
            if np[i].label()=='NP':
                if i>0:
                    if len(np[i-1])>1:
                        if np[i-1][1]=='CC':
                            return False;
                    if np[i-1][0]=='of':
                        if i>1:
                            return if_single_n(np[i-2])
                        else:
                            print('error! There is something wrong with "if_single_n", please tell gjy "jaygao1219@gmail.com"')
                            print(np)
                            return False
                return if_single_n(np[i]);
            if np[i].label()=='N':
                if np[i][0][1] in ['NN','NNP','CD']:
                    return True;
                return False
            pass;
        pass;
    print('error! There is something wrong with "if_single_n", please tell gjy "jaygao1219@gmail.com"')
    print(np)
    return False

def fit_single_v(vp):#检查是否是第三人称，一般现在时，现在进行时，一般过去时，现在完成时，过去进行时，现在完成进行时,并给出修改建议,目前没有考虑不规则动词
    if vp.label()=='VP':
        return fit_single_v(vp[0])
    if len(vp)==1:
        if vp[0][1] in ['VBP']:
            return (vp[0][0],vp[0][0]+'s');
        return True;
    for g in groups:
        if vp[0][0]==g[0]:
            return (g[0],g[1])
    return True

def Verb_third_singular(num,content):
    c=word_callout(content)
    cp=nltk.RegexpParser(g1)
    result=cp.parse(c)
    l=len(result)
    wrongs=[]
    for i in range(l):
        if type(result[i])==nltk.tree.Tree:
            if result[i].label()=='ROOT':
                rr=len(result[i])
                for j in range(rr-1):
                    if result[i][j].label()=='NP' or result[i][j]=='PRP':
                        if result[i][j+1].label()=='VP' or result[i][j+1].label()=='V':
                            if if_single_n(result[i][j]):
                                cur=fit_single_v(result[i][j+1])
                                if cur!=True:
                                    wrongs.append((num,i,j+1,cur))
                                    pass;
                                pass;
                            pass;
                        pass;
                    pass;
                pass;
            pass;
        pass;
    current=[]
    for w in wrongs:
        begin=content.find(w[3][0])
        end=begin+len(w[3][0])
        current.append((begin+num,end+num,w[3][1]))
    return current

def check(content):#content[num]是这里面的值
    sce=""
    begin=0#开始的位置
    result=[]
    for c in range(len(content)):
        if content[c] in ['.',';',':','?','!']:
            if sce:
                sce=sce+content[c]
                if c<len(content)-1:
                    cur=Verb_third_singular(begin,sce)
                    if cur:
                        result.append(cur)
                    begin=begin+len(sce)
                    sce=""
                    pass;
            pass;
        else:
            sce=sce+content[c]
            pass;
        pass;
    return result

if __name__=='__main__':
    print(check(scentence))
