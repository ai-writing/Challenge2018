#encoding:utf-8
#verbset2lemma.py 读入verbset,遍历文字,写出ldict和cldict

import numpy as np
import word2vec
import re
import time
import os
import pickle
import random
import requests
import json
from queue import Queue
#bug:shorten和shorten_front不一样的话,每一遍都得重新计算而不是直接从队列里拿出来!


class reader(object):
    def printtag(self,number):
        #names=['现在式','现在式第三人称单数','现在式非第三人称单数','过去式','过去分词','现在分词']
        if number==len(self.verbtags):
            return 'NN'
        return self.verbtags[number]
        #return names[number]
    def parse(self,text):
        if(text==''):
            raise NameError
        url = 'http://166.111.139.15:9000'
        params = {'properties' : r"{'annotators': 'tokenize,ssplit,pos,lemma,parse', 'outputFormat': 'json'}"}
        while True:
            try:
                temptime=time.time()
                resp = requests.post(url, text, params=params).text
                content=json.loads(resp)
                self.numtopos=[]
                for i in content['sentences']:
                    temppos=[0]*len(i['tokens'])
                    for j in i['tokens']:
                        temppos[j['index']-1]=[j['characterOffsetBegin'],j['characterOffsetEnd']]
                    self.numtopos.append(temppos)


                #print( re.sub('\s+',' ',content['sentences'][:]['parse'].replace('\n',' ')))
                #return re.sub('\s+',' ',content['sentences'][:]['parse'].replace('\n',' '))
                return [i['parse'] for i in content['sentences']]
            except:# ConnectionRefusedError:
                print('Stnlp connection refused. Retrying...',time.time()-temptime)
                print(resp)
    def __init__(self,\
                content,\
                patchlength=3,\
                maxlength=700,\
                embedding_size=100,\
                num_verbs=1,\
                allinclude=True,\
                passnum=0):   #几句前文是否shorten #是否输出不带tag,只有单词的句子 

#patchlength:每次输入前文额外的句子的数量.
#maxlength:每句话的最大长度.(包括前文额外句子).超过该长度的句子会被丢弃.
#embedding_size:词向量维度数.
        self.url = 'http://166.111.139.15:9000'
        self.patchlength=patchlength
        self.maxlength=maxlength
        self.embedding_size=embedding_size
        self.num_verbs=num_verbs
        self.allinclude=allinclude
        self.passnum=passnum
        self.verbtags=['VB','VBZ','VBP','VBD','VBN','VBG'] #所有动词的tag

        
        dir0='papersmith/editor/grammar/tense/'
        dir0='tense/'
        #print('0')
        #self.model=[]
        #print('1')
        self.oldqueue=Queue()

        #parse
        self.resp=self.parse(content)
        self.readlength=len(self.resp)
        self.readlength=10
        #print('rdlng',self.readlength)
        self.pointer=0
#        self.pointer=45521*50+4363449
        for _ in range(self.patchlength):
            self.oldqueue.put(self.resp[0])

#加载原型词典(把动词变为它的原型)
        self.ldict ={}
        with open(dir0+'tagdict', 'rb') as f:
            self.tagdict = pickle.load(f)
        self.cldict ={}
        with open(dir0+'verbset', 'rb') as f:
            self.verbset = pickle.load(f)
        

    def lemma(self,verb,tag):
        if verb in self.ldict:
            return self.ldict[verb]
        else:
            params = {'properties' : r"{'annotators': 'lemma', 'outputFormat': 'json'}"}
            resp = requests.post(self.url, verb, params=params).text
            content=json.loads(resp)
            word=content['sentences'][0]['tokens'][0]['lemma']
            print('errverb',verb)
            self.ldict[verb]=word
            self.cldict[word+'('+tag]=verb
            return word

    def list_tags(self,batch_size):
        while True:#防止读到末尾
                if self.pointer==self.readlength:
                    with open(dir0+'ldict5','wb') as f:
                        pickle.dump(ldict,f)
                    with open(dir0+'cldict5','wb') as f:
                        pickle.dump(cldict,f)
                    
                    print('epoch')
                if self.pointer%2000==0:
                    print(self.pointer)

                sentence=self.resp[self.pointer]
                self.pointer+=1

#筛选只有一个动词的句子                
                for tag in sentence.split():
                    if tag[0]=='(':
                        if tag[1:] in self.verbtags:
                            flag=1
                            odtag=tag[1:]
                        else:
                            flag=0
                    elif flag==1:
                        lemma(verb,odtag)


if __name__ == '__main__':
    with open('tense/combine.txt') as f:
            model = reader(f.readline())
            model.list_tags(1)

