#encoding:utf-8
#注意 batchsize是50,提高速度但是扔掉最后不足50的部分.

class Tense(object):

    def __init__(self):
        self.passflag=0
        try:
            import word2vec
            import requests
            import numpy as np
            import tensorflow as tf
            import time
            import os
            os.environ["CUDA_VISIBLE_DEVICES"]=""#环境变量：使用第一块gpu
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
        self.batch_size=20

#input
        self.model=tensernnmodel.rnnmodel(vocab_single=6,\
                    maxlength=700,\
                    embedding_size=100,\
                    batch_size=self.batch_size,\
                    num_verbs=1)

        with open(self.dir0+'cldict','rb') as f:
            self.cldict=pickle.load(f)

        self.sessionlist=[]
        for i in range(4):
            session=tf.Session(config=self.config)
            session.run(tf.global_variables_initializer())#初始化变量
            saver=tf.train.Saver()
            ckpt = tf.train.get_checkpoint_state(self.dir0+'p'+str(i)+'n1')
            if ckpt==None:
                print('checkpoint not found. skip tense.')
                return
            saver.restore(session, ckpt.model_checkpoint_path)
            self.sessionlist.append(session)






    def work(self,verse):
        if self.passflag==1:
            print('not installed packages. skip tense.')
            return []
        import word2vec
        import requests
        import numpy as np
        import tensorflow as tf
        import time
        import os
        os.environ["CUDA_VISIBLE_DEVICES"]=""#环境变量：使用第一块gpu
        import pickle
        import sys, getopt
        #from papersmith.editor.grammar import tensereader
        #from papersmith.editor.grammar import tensernnmodel 
        import tensereader
        self.reader=tensereader.reader(verse)
        #print('start session')

#multi-time test
        suggests=[]
        while True:
            inputs,pads,poses,words,total,answers=self.reader.list_tags(self.batch_size)
            if inputs==None:
                return suggests
            for multitime in range(3):
                suggestion=self.worksess(multitime,inputs,pads,poses,words,total,answers)
                suggests.extend(suggestion)

    def worksess(self,multitime,inputs,pads,poses,words,total,answers):
        import word2vec
        import requests
        import numpy as np
        import tensorflow as tf
        import time
        import os
        os.environ["CUDA_VISIBLE_DEVICES"]=""#环境变量：使用第一块gpu
        import pickle
        import sys, getopt
        suggests=[]
        #from papersmith.editor.grammar import tensereader
        #from papersmith.editor.grammar import tensernnmodel 
        session=self.sessionlist[multitime]
        pred=session.run([self.model.pred],  feed_dict={self.model.x: inputs, self.model.p:pads})[0]

        #print(answers,pred)
        #print(tf.argmax(pred[0]).eval(session=session) )
        for i in range(len(pred)):
            if len(answers[i])<=multitime:
                continue
            if tf.argmax(pred[i]).eval(session=session) != answers[i][multitime]:
                mem=tf.argmax(pred[i]).eval(session=session)
                pred[i][tf.argmax(pred[i]).eval(session=session)]=-100
                if tf.argmax(pred[i]).eval(session=session) != answers[i][multitime]:
                    pred[i][tf.argmax(pred[i]).eval(session=session)]=-100
                    if tf.argmax(pred[i]).eval(session=session) != answers[i][multitime]:
                        level=1
                    else:
                        level=2

                    try:
                        temp=poses[i][multitime][:]
                        newword=self.cldict[self.reader.lemma(words[i][multitime])+'('+self.reader.printtag(mem)]
                        if(newword!=words[i][multitime]):
                            temp.append(newword)
                        #temp.append(words[i][multitime]+' '+self.reader.printtag(answers[i][multitime])+'改为'+self.reader.printtag(mem))
                            temp.append(level)
                            suggests.append(temp)
                    except:
                        print('err')
                        pass
        print('worksess: ',multitime,'sug', suggests)
#        pred=pred[0]
        return suggests
        #print(pred,type(pred))
#累加计算平均正确率

if __name__=='__main__':
    tensechecker=Tense()
#print(tensechecker.work("The fox is big, grew bigger. The rat was small but runs quickly. The fox is big, grew bigger. The rat was small but runs quickly."))
    with open('testinput4.txt') as f:
        content=f.read()
        result=tensechecker.work(content)
        print('num:',len(result))
        print('result:',result)
        for i in result:
            print(content[i[0]-50:i[0]]+'('+content[i[0]:i[1]]+')'+content[i[1]:i[1]+50]+'\nchange to: '+str(i[2])+' level: '+str(i[3])+'\n')
