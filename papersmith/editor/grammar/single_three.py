#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'grammer correcting'

__author__='Jay Gao 1219'

import nltk
import nltk.data

scentence="""In 2014, he says the first workshop about the creative community. It had attracted more than 40 people from government agencies, social organizations, business circles, IT experts and design professional teachers and students to participate. The design of the six teams are based on Internet.

Communication technology such as Internet of things, sensor network and so on, so as to form a new management form community based on large-scale information intelligent processing.

Six teams results varied, respectively: the design of electronic waste recycling platform, the prototype design of community old-age self-help, the design of remote control robot, Babel Tower breaker Bracelet design, the design of the joint office, commercial exhibition and creative communication space design and the design of City pet dog intelligence community.
"""

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
def SplitPargraph(string):
    tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
    string=tokenizer.tokenize(string)
    return string;

def word_callout(string):
    string=nltk.word_tokenize(string)
    string=nltk.pos_tag(string)
    return string

def if_single_n(np):#('we', 'PRP')
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

def fit_single_v(vp):#检查是否是第三人称，一般现在时，现在进行时，一般过去时，现在完成时，过去进行时，现在完成进行时 
    if vp.label()=='VP':
        return fit_single_v(vp[0])
    if len(vp)==1:
        if vp[0][1] in ['VBP']:
            return False;
        return True;
    if vp[0][0] in ['are','am','have','were']:
        return False;
    return True


def Verb_third_singular(num,content):
    c=word_callout(content)
    cp=nltk.RegexpParser(g1)
    result=cp.parse(c)
    l=len(result)
    wrongs=[]
    print(result)
    for i in range(l):
        if type(result[i])==nltk.tree.Tree:
            if result[i].label()=='ROOT':
                rr=len(result[i])
                for j in range(rr-1):
                    if result[i][j].label()=='NP' or result[i][j]=='PRP':
                        if result[i][j+1].label()=='VP' or result[i][j+1].label()=='V':
                            if if_single_n(result[i][j]):
                                if fit_single_v(result[i][j+1])==0:
                                    wrongs.append((num,i,j))
                                    pass;
                                pass;
                            pass;
                        pass;
                    pass;
                pass;
            pass;
        pass;
    return wrongs;

if __name__=='__main__':
    scentence=SplitPargraph(scentence)
    result=[]
    for s in range(len(scentence)):
        result.append(Verb_third_singular(s,scentence[s]))
        pass;
    print(result)
