#encoding:utf-8
#run3.py 只看含有两个动词的句子

import numpy as np
import tensorflow as tf
import time
import os
import pickle
import sys, getopt
import papersmith.editor.grammar.tensereader
import papersmith.editor.grammar.tensernnmodel 




def tensecheck(verse):
    dir0='Challenge2018/blob/dev/papersmith/editor/grammar/tense/'

    reader=tensereader.reader(verse)


#神经网络的输入是一句只有一个动词的句子（以及其语法树），把动词变为原型，语法树的tag变为了VB。
#并预测它的动词时态。如果它不为0，输入变为这句话以及他前面的patchlength句话。
#语法树结构：（VB love）会被变为三个标签：（VB的（100维）one-hot标签，love的词向量标签，反括号对应的全0标签。
#每个反括号对应一个单独的标签，而正括号没有。

    patchlength=3                   #输入的前文句子的数量
    embedding_size=100              #词向量维度数量
    maxlength=700                   #输入序列最大长度
    num_verbs=1                     #一次看两个动词

    time_verbose_flag=False         #测量输入和运行的时间比



    config=tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction=0.45#占用45%显存
    config.gpu_options.allow_growth = True

    testflag=True
    loadold=True
    batch_size=1
    saving_step=100000000000
    display_step=10000000000

#        config.device_count={'gpu':0}#使用cpu

    multiflag=True
    multinum=4




#input

    model=tensernnmodel.rnnmodel(vocab_single=6,\
                maxlength=maxlength,\
                embedding_size=embedding_size,\
                batch_size=1,\
                num_verbs=1)

    saver=tf.train.Saver()
    with open(dir0+'cldict','rb') as f:
        cldict=pickle.load(f)
    #print('start session')

#multi-time test
    suggests=[]
    while True:
        multitime=0
        while True:
            #print('nut,',multitime)

            with tf.Session(config=config) as session:
                session.run(tf.global_variables_initializer())#初始化变量
                ckpt = tf.train.get_checkpoint_state(dir0+'p'+str(multitime)+'n1')
                #print('p'+str(multitime)+'n1')
                saver.restore(session, ckpt.model_checkpoint_path)
#读入一个batch的数据
#重用的话只要实现自己的reader.py就行.
#输出:count:指针,指向读到文件的哪个位置
#inputs:batch_size个输入句子,形状为[batch_size, maxlength, embedding_size]
#pads:batch内每句话的长度,形状为[batch_size]
#answers:输入的答案,形状为[batch_size,vocab_size]
                    #print('i')
                    #print('b',batch_size)
                        #print('listtags')
                if multitime==0:
                    inputs,pads,poses,words,total,answers=reader.list_tags(1)
                    #print('inputs:',inputs,pads,poses,total,answers)
                    if inputs==None:
                        return suggests
                    total=min(total,multinum)
                        #print('sv',singleverb)
#运行一次
                pred=session.run([model.pred],  feed_dict={model.x: inputs, model.p:pads})[0]

                
                for i in range(len(pred)):
                    if tf.argmax(pred[i]).eval() != answers[i]:
                        pred[i][tf.argmax(pred[i]).eval()]=-100
                        if tf.argmax(pred[i]).eval() != answers[i]:
                            temp=poses[multitime]
                            temp.append(cldict[reader.lemma(words[multitime])+'('+reader.printtag(tf.argmax(pred[i]).eval())])
                            suggests.append(temp)
                            #print(suggests)
                pred=pred[0]
                #print(pred,type(pred))
#累加计算平均正确率
                multitime+=1
                if multitime>=total:
                    break

#print('sug',tensecheck('The fox was big.'))
