#encoding:utf-8
#注意!没做nounflag.需要的去reader.py取

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
#        return [k for k, v in self.verbtags.items() if v == number][0]
        return self.verbtags[number]
    def parse(self,text):
        #print('start parse')
        if(text==''):
            raise NameError
        url = 'http://166.111.139.15:9000'
        params = {'properties' : r"{'annotators': 'tokenize,ssplit,pos,lemma,parse', 'outputFormat': 'json'}"}
        while True:
            try:
                resp = requests.post(url, text, params=params).text
                content=json.loads(resp)
                #print('finish parse:',re.sub('\s+',' ',content['sentences'][0]['parse'].replace('\n',' ')))
                return re.sub('\s+',' ',content['sentences'][0]['parse'].replace('\n',' '))
            except ConnectionRefusedError:
                print('error, retrying...')

    def clean(self,sentence):
        initial=''
        for tag in sentence.split():
            if tag[0]=='(':
                if tag[1:] in self.verbtags:
                    vbflag=1
                else:
                    vbflag=0
            else:
                node=re.match('([^\)]+)(\)*)',tag.strip())
                if node:
                    if vbflag==1:
                        initial+=' ('+node.group(1)+')'
                    else:
                        initial+=' '+node.group(1)
        return initial
    def cleanclear(self,sentence):
        initial=''
        for tag in sentence.split():
            if tag[0]=='(':
                if tag[1:] in self.verbtags:
                    vbflag=1
                else:
                    vbflag=0
            else:
                node=re.match('([^\)]+)(\)*)',tag.strip())
                if node:
                    initial+=' '+node.group(1)
        return initial
    def work(self,a,posdict):
        url = 'http://166.111.139.15:9000'
        params = {'properties' : r"{'annotators': 'tokenize,ssplit,pos,lemma,parse,depparse', 'outputFormat': 'json'}"}
        while True:
            try:
                resp = requests.post(url,a,params=params).text
                break
            except ConnectionRefusedError:
                print('error, retrying...')
#        print(resp)
#        input()
        try:
            content=json.loads(resp)
        except:
            print('resperror: ',resp)
            return 1
        for sentence in content['sentences']:
            for i in sentence['enhancedPlusPlusDependencies']:
                for j in i:
                    if i['dep']=='nsubjpass':
                        #print(i)
                        #input()
#                        print(posdict)
                        if posdict[i['governor']]<4:
 #                           print(':\n',a,posdict[i['governor']]+1)
                            return posdict[i['governor']]+1
                        else:
                            return 0
        return 0

    def isverb(self,verb):
        if verb not in self.ldict: return False
        for i in self.verbtags:
            if (self.ldict[verb]+'('+i) not in self.cldict: return False
        return True
        

    def __init__(self,\
                patchlength=3,\
                maxlength=700,\
                embedding_size=100,\
                num_verbs=2,\
                allinclude=False,\
                shorten=False,\
                shorten_front=False,\
                testflag=False,\
                passnum=0,\
                nounflag=False,\
                dpflag=False):   #几句前文是否shorten #是否输出不带tag,只有单词的句子 

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
        self.passnum=passnum
        print('pas',passnum)
        self.verbtags=['VB','VBZ','VBP','VBD','VBN','VBG'] #所有动词的tag
        self.model=word2vec.load('train/combine100.bin')   #加载词向量模型
        print('loaded model')
        self.oldqueue=Queue()
        self.testflag=testflag

        self.testfile=open('input.txt')
        if testflag==False:
            self.resp=open(r'train/resp2').readlines()
            self.readlength=len(self.resp)
            print('readlength',self.readlength)
            self.pointer=random.randint(0,self.readlength-1)
#            self.pointer=1621919
            print('pointer',self.pointer)
            for _ in range(self.patchlength):
                self.oldqueue.put(self.resp[self.pointer])
                self.pointer+=1
        else:
            for _ in range(self.patchlength):
                if shorten_front==True:
                    #self.oldqueue.put(input('0:type sentence:'))
                    self.oldqueue.put(self.testfile.readline())
                else:
                    #self.oldqueue.put(self.parse(input('0:type sentence:')))
                    self.oldqueue.put(self.parse(self.testfile.readline()))

#加载文字

#加载原型词典(把动词变为它的原型)
        with open('train/ldict2', 'rb') as f:
            self.ldict = pickle.load(f)
        with open('train/tagdict', 'rb') as f:
            self.tagdict = pickle.load(f)
        with open('train/cldict', 'rb') as f:
            self.cldict = pickle.load(f)
        

    def isverb(self,verb):
        if verb not in self.ldict: return False
        for i in self.verbtags:
            if (self.ldict[verb]+'('+i) not in self.cldict: return False
        return True




    def lemma(self,verb):
        if verb in self.ldict:
            return self.ldict[verb]
        else:
            params = {'properties' : r"{'annotators': 'lemma', 'outputFormat': 'json'}"}
            resp = requests.post(self.url, verb, params=params).text
            content=json.loads(resp)
            word=content['sentences'][0]['tokens'][0]['lemma']
            self.ldict[verb]=word
            print('errorverb: ',verb,word)
            return word

    def list_tags(self,batch_size):
        while True:#防止读到末尾
            inputs=[]
            pads=[]
            answer=[]
            count=0
            while len(answer)<batch_size:
                #print('batch_size',batch_size)

                if self.testflag==True:
                    if self.shorten==True:
                        #sentence=input('1:')
                        sentence=self.testfile.readline()
                    else:
                        #print('parsed!')
                        #sentence=self.parse(input('1:'))
                        sentence=self.parse(self.testfile.readline())
                else:
                    sentence=self.resp[self.pointer]
                    if len(sentence)>20000:
                        print('pointer',self.pointer)
                        raise MemoryError
                    self.pointer+=1
                    #print(self.pointer)
                    if self.pointer==self.readlength:
                        self.pointer=0
                        print('epoch')

                outword=[]
                total=0
                singleverb=0
#筛选只有一个动词的句子                
                for tag in sentence.split():
                    if tag[0]!='(':
                        node=re.match('([^\)]+)(\)*)',tag.strip())
                        if node:
                            if isverb(node.group(1)):
                                total+=1
                if (self.allinclude==True and total<(self.num_verbs+self.passnum)) or (self.allinclude==False and total!=(self.num_verbs+self.passnum)):
                    self.oldqueue.put(sentence)
                    self.oldqueue.get()
                    #print('short')
                    continue
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
                posdict=dict()
                verbcount=0
                wordcount=0

#本句                
                for tag in sentence.split():
                    if tag[0]=='(':
#去除情态动词
                        if tag=='(MD':
                            mdflag=1
                        else:
                            mdflag=0
                            if tag[1:] in self.verbtags:
                                if dpflag==False:
                                    if singleverb==self.passnum:
                                        answer.append(self.verbtags.index(tag[1:]))
                                    elif singleverb>self.passnum and singleverb<self.num_verbs+self.passnum:
                                        answer[-1]*=len(self.verbtags)
                                        answer[-1]+=self.verbtags.index(tag[1:])
                                    singleverb+=1
                                tag='(VB'
                                vbflag=1
                            else:
                                vbflag=0
                            if tag not in self.tagdict:
                                self.tagdict[tag]=len(self.tagdict)
                                print(len(self.tagdict))
                            tagword=[0]*self.embedding_size
                            tagword[self.tagdict[tag]]=1
                            if not self.shorten:
                                outword.append(tagword)
                    else:
                        wordcount+=1
                        if mdflag==0:
                            node=re.match('([^\)]+)(\)*)',tag.strip())
                            if node:
                                verb=node.group(1)
                                if verb in self.model:
                                    if vbflag==1 or isverb(verb):
                                        if vbflag==0:
                                            if dpflag==True:
                                                answer.append(len(self.verbtags))
                                            else:
                                                if singleverb==self.passnum:
                                                    answer.append(len(self.verbtags))
                                                elif singleverb>self.passnum and singleverb<self.num_verbs+self.passnum:
                                                    answer[-1]*=len(self.verbtags)
                                                    answer[-1]+=len(self.verbtags)
                                                singleverb+=1

                                            
#去除时态
                                        node2=self.lemma(verb)
                                        if node2 in self.model:
                                            if dpflag==True:
                                                if not (node2=='is' or node2=='have'):#去除is,have

                                                    posdict[wordcount]=verbcount
                                                    verbcount+=1
                                                    outword.append(self.model[node2].tolist())
                                            else:
                                                outword.append(self.model[node2].tolist())


                                        else:
                                            outword.append([0]*self.embedding_size)
                                    else:
                                        outword.append(self.model[verb].tolist())
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
                    if dpflag==False and singleverb>0:
                        answer=answer[:-1]
                    print('toolong')
                    continue
                if dpflag==True:
                    temp=[0]*5
                    qq=self.work(self.cleanclear(sentence),posdict)
                    temp[qq]=1
            #        print(self.clean(sentence),qq)
            #        input()
                    answer.append(temp)
#补零
                pads.append(outword.shape[0])
                outword=np.pad(outword,((0,self.maxlength-outword.shape[0]),(0,0)),'constant')
                inputs.append(outword)

            inputs=np.array(inputs)
#构建输出
            if dpflag==False:
                answers=np.zeros((len(answer),pow(len(self.verbtags),self.num_verbs)))
                for num in range(len(answer)):
                    answers[num][answer[num]]=1
                answer=answers
#用完整个输入,从头开始
#continue the 'while True' loop
            return inputs,pads,answer,singleverb

if __name__ == '__main__':
    model = reader()
    for i in range(2):
        model.list_tags(1)
