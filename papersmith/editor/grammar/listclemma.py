#encoding:utf-8
#reader.py 只看含有一个动词的句子(十分之一左右)

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
    def parse(self,text):
        print('parse')
        params = {'properties' : r"{'annotators': 'tokenize,ssplit,pos,lemma,parse', 'outputFormat': 'json'}"}
        while True:
            try:
                resp = requests.post(self.url, input(), params=params).text
                content=json.loads(resp)
                return re.sub('\s+',' ',content['sentences'][0]['parse'].replace('\n',' '))
            except:
                print('error, retrying...')
    def __init__(self,\
                patchlength=3,\
                maxlength=700,\
                embedding_size=100,\
                num_verbs=2,\
                allinclude=False,\
                shorten=False,\
                shorten_front=False,\
                testflag=False):   #几句前文是否shorten #是否输出不带tag,只有单词的句子 

#patchlength:每次输入前文额外的句子的数量.
#maxlength:每句话的最大长度.(包括前文额外句子).超过该长度的句子会被丢弃.
#embedding_size:词向量维度数.
        self.url = 'http://166.111.139.15:9000'
        self.shorten=shorten
        self.shorten_front=shorten_front   #几句前文是否shorten #是否输出不带tag,只有单词的句子 
        self.patchlength=patchlength
        self.maxlength=maxlength
        self.embedding_size=embedding_size
        self.num_verbs=num_verbs
        self.allinclude=allinclude
        self.verbtags=['VB','VBZ','VBP','VBD','VBN','VBG'] #所有动词的tag
        self.model=word2vec.load('tense/combine100.bin')   #加载词向量模型
        self.tagdict={')':0}
        print('loaded model')
        self.oldqueue=Queue()
        self.testflag=testflag
        if testflag==False:
            self.resp=open(r'tense/resp2').readlines()
            self.readlength=len(self.resp)
            print('readlength',self.readlength)
#            self.pointer=random.randint(0,self.readlength-1)
            self.pointer=0
            print('pointer',self.pointer)
            for _ in range(self.patchlength):
                self.oldqueue.put(self.resp[self.pointer])
                self.pointer+=1
        else:
            for _ in range(self.patchlength):
                if shorten_front==True:
                    self.oldqueue.put(input())
                else:
                    self.oldqueue.put(self.parse(input()))

        self.cldict=dict()
#加载文字

#加载原型词典(把动词变为它的原型)
        with open('tense/ldict2', 'rb') as f:
            self.ldict = pickle.load(f)
        with open('tense/tagdict', 'rb') as f:
            self.tagdict = pickle.load(f)
        with open('tense/cldict', 'rb') as f:
            self.cldictori = pickle.load(f)

        print('loaded lemma')

    def isverb(self,verb):
        if verb not in self.ldict: return False
        for i in self.verbtags:
            if (self.ldict[verb]+'('+i) not in self.cldictori: return False
        return True



    def lemma(self,verb,tag):
        if verb in self.ldict:
            word=self.ldict[verb]
            if (word+tag) not in self.cldict:
                self.cldict[word+tag]={verb:1}
            else:
                if verb in self.cldict[word+tag]:
                    self.cldict[word+tag][verb]+=1
                else:
                    self.cldict[word+tag][verb]=1

            return word
        else:
            params = {'properties' : r"{'annotators': 'lemma', 'outputFormat': 'json'}"}
            resp = requests.post(self.url, verb, params=params).text
            content=json.loads(resp)
            word=content['sentences'][0]['tokens'][0]['lemma']
            self.ldict[verb]=word
            self.cldict[word+tag]=verb
            return word

    def list_tags(self,batch_size):
        while True:#防止读到末尾
            inputs=[]
            pads=[]
            answer=[]
            count=0
            while len(answer)<batch_size:

                if self.testflag==True:
                    if shorten==True:
                        sentence=input()
                    else:
                        sentence=self.parse(input())
                else:
                    sentence=self.resp[self.pointer]
                    if len(sentence)>20000:
                        print('pointer',self.pointer)
                        raise MemoryError
                    self.pointer+=1
                    if self.pointer==self.readlength:
                        self.pointer=0
                        print('epoch')
                        with open('tense/ldictor','wb') as f2:
                            pickle.dump(self.ldict,f2)
                        with open('tense/cldictor','wb') as f2:
                            pickle.dump(self.cldict,f2)
                        with open('tense/cldict3','wb') as f2:
                            cldict2=dict()
                            for i in self.cldict:
                                maxf=0
                                for j in i:
                                    if maxf<self.cldict[i][j]:
                                        maxf=self.cldict[i][j]
                                        cldict2[i]=j
                            pickle.dump(cldict2,f2)
                        return

                outword=[]
                total=0
                singleverb=0
#筛选只有一个动词的句子                
                for tag in sentence.split():
                    if tag[0]=='(':
                        if tag[1:] in self.verbtags:
                            total+=1
#前文句子
                newqueue=Queue()
                for _ in range(self.patchlength):
                    oldsentence=self.oldqueue.get()
                    newqueue.put(oldsentence)
                    for tag in oldsentence.split():
                        if tag[0]=='(':
                            if tag not in self.tagdict:
                                self.tagdict[tag]=len(self.tagdict)
                                print(len(self.tagdict))
                            tagword=[0]*self.embedding_size
                            tagword[self.tagdict[tag]]=1
                            if not self.shorten_front:
                                outword.append(tagword)
                        else:                
                            node=re.match('([^\)]+)(\)*)',tag.strip())
                            if node:
                                #group(1) 单词
                                if node.group(1) in self.model:
                                    outword.append(self.model[node.group(1)].tolist())
                                else:
                                    outword.append([0]*self.embedding_size)
                                #group(2) 括号
                                if not self.shorten_front:
                                    tagword=[0]*self.embedding_size
                                    tagword[0]=1
                                    for _ in range(len(node.group(2))-1):
                                        outword.append(tagword)
                self.oldqueue=newqueue
                self.oldqueue.put(sentence)
                self.oldqueue.get()
                #print('point at:',self.resp.tell())

#本句                
                for tag in sentence.split():
                    if tag[0]=='(':
#去除情态动词
                        if tag=='(MD':
                            mdflag=1
                        else:
                            mdflag=0
                            if tag[1:] in self.verbtags:
                                vbflag=1
                                tagold=tag
                            else:
                                vbflag=0
                            if tag not in self.tagdict:
                                self.tagdict[tag]=len(self.tagdict)
                                print('tag',len(self.tagdict))
                            tagword=[0]*self.embedding_size
                            tagword[self.tagdict[tag]]=1
                            if not self.shorten:
                                outword.append(tagword)
                    else:
                        if mdflag==0:
                            node=re.match('([^\)]+)(\)*)',tag.strip())
                            if node:
                                if node.group(1) in self.model:
                                    if vbflag==1 or self.isverb(node.group(1)):
#去除时态
                                        node2=self.lemma(node.group(1),tagold)
                                        if node2 in self.model:
                                            outword.append(self.model[node2].tolist())
                                        else:
                                            outword.append([0]*self.embedding_size)
                                    else:
                                        outword.append(self.model[node.group(1)].tolist())
                                else:
                                    outword.append([0]*self.embedding_size)
                                if not self.shorten:
                                    tagword=[0]*self.embedding_size
                                    tagword[0]=1
                                    for _ in range(len(node.group(2))-1):
                                        outword.append(tagword)
                outword=np.array(outword)
#句子过长
                if outword.shape[0]>self.maxlength:
#                    print('pass')
                    answer=answer[:-1]
                    continue
#补零
#构建输出
#用完整个输入,从头开始
#continue the 'while True' loop

if __name__ == '__main__':
    model = reader()
    model.list_tags(5000000000000)
