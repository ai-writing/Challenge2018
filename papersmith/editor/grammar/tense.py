#encoding:utf-8
#run3.py 只看含有两个动词的句子

class Tense(object):

    def __init__():
        self.passflag=0
        try:
            import word2vec
            import requests
            import json
            import numpy as np
            import tensorflow as tf
            import time
            import os
            import pickle
            import sys, getopt
            #from papersmith.editor.grammar import tensereader
            #from papersmith.editor.grammar import tensernnmodel 
            import tensereader
            import tensernnmodel 
        except:
            self.passflag=1
            print('not installed packages. skip tense.')
            return

        #dir0='papersmith/editor/grammar/tense/'
        self.dir0='tense/'
#神经网络的输入是一句只有一个动词的句子（以及其语法树），把动词变为原型，语法树的tag变为了VB。
#并预测它的动词时态。如果它不为0，输入变为这句话以及他前面的patchlength句话。
#语法树结构：（VB love）会被变为三个标签：（VB的（100维）one-hot标签，love的词向量标签，反括号对应的全0标签。
#每个反括号对应一个单独的标签，而正括号没有。
        self.config=tf.ConfigProto()
        self.config.gpu_options.per_process_gpu_memory_fraction=0.45#占用45%显存
        self.config.gpu_options.allow_growth = True

#input
        self.model=tensernnmodel.rnnmodel(vocab_single=6,\
                    maxlength=700,\
                    embedding_size=100,\
                    batch_size=1,\
                    num_verbs=1)

        with open(self.dir0+'cldict','rb') as f:
            self.cldict=pickle.load(f)

        self.sessionlist=[]
        for i in range(4):
            session=tf.Session(config=config)
            session.run(tf.global_variables_initializer())#初始化变量
            saver=tf.train.Saver()
            ckpt = tf.train.get_checkpoint_state(self.dir0+'p'+str(multitime)+'n1')
            if ckpt==None:
                print('checkpoint not found. skip tense.')
                return []
            saver.restore(session, ckpt.model_checkpoint_path)
            self.sessionlist.append(session)






    def work(verse):
        if self.passflag==1:
            print('not installed packages. skip tense.')
            return []
        self.reader=tensereader.reader(verse)
        #print('start session')

#multi-time test
        suggests=[]
        while True:
            inputs,pads,poses,words,total,answers=self.reader.list_tags(1)
            if inputs==None:
                return suggests
            for multitime in range(min(total,4)):
                suggestion=self.worksess(multitime,inputs,pads,poses,words,total,answers)
                suggests.extend(suggestion)

    def worksess(multitime,inputs,pads,poses,words,total,answers):
        session=sessionlist[multitime]
        pred=session.run([self.model.pred],  feed_dict={self.model.x: inputs, self.model.p:pads})[0]

        #print(answers,pred)
        #print(tf.argmax(pred[0]).eval() )
        for i in range(len(pred)):
            if tf.argmax(pred[i]).eval() != answers[i][multitime]:
                mem=tf.argmax(pred[i]).eval()
                pred[i][tf.argmax(pred[i]).eval()]=-100
                if tf.argmax(pred[i]).eval() != answers[i][multitime]:
                    temp=poses[multitime]
                    temp.append(self.cldict[self.reader.lemma(words[multitime])+'('+self.reader.printtag(mem)])
                    #temp.append(words[multitime]+' '+self.reader.printtag(answers[i][multitime])+'改为'+self.reader.printtag(mem))
                    temp.append(1)
                    suggests.append(temp)
                else:
                    temp=poses[multitime]
                    temp.append(self.cldict[self.reader.lemma(words[multitime])+'('+self.reader.printtag(mem)])
                    #temp.append(words[multitime]+' '+self.reader.printtag(answers[i][multitime])+'改为'+self.reader.printtag(mem))
                    #print(cldict)
                    temp.append(2)
                    suggests.append(temp)
                    #print(suggests)
        pred=pred[0]
        #print(pred,type(pred))
#累加计算平均正确率

print('sug',tensecheck('The fox was big, grows bigger.'))
