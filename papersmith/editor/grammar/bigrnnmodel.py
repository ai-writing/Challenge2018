#encoding:utf-8
#rnnmodel3.py 针对两个动词
#learning rate decay
#patchlength 0 readfrom resp
#add:saving session
from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib import rnn

class rnnmodel(object):
    def __init__(self,\
                vocab_single=6,\
                maxlength=200,\
                embedding_size=100,\
                initial_training_rate=0.001,\
                batch_size=1,\
                num_verbs=2):

#针对多个动词:
        vocab_size=pow(vocab_single,num_verbs)
#learning_rate 可依次递减.然而global_step好像只能在run里每train一次+1,而不能写在这个init函数里?不太清楚.
#每500步变为原来的0.8倍,指数递减.
        self.global_step = tf.Variable(0, trainable=False)
        self.learning_rate = tf.train.exponential_decay(initial_training_rate, global_step=self.global_step, decay_steps=500,decay_rate=0.8)

#输入信息.
#x:输入的数据.batch_size是每次输入的数据的多少.大致是越多越精确,不过越多数据用得越快,需要多循环用几次.而且越多吃的显存越多,太大会报错.
#也有可能设置得太大导致无法学习的情况.
#maxlength为输入的序列最大长度,也就是一个句子最多有几个词.
#embedding_size是表示每个词的词向量的维度数.
        self.x = tf.placeholder("float", [batch_size, maxlength, embedding_size])

#输入信息对应的答案.
#vocab_size是输出数据的维度数.
#这是一个单分类问题,输出为预测的6种时态各自的可能性.
        self.y = tf.placeholder("float", [batch_size, vocab_size])

#pad长度.
#这里输入一个batch中每句话的长度(int).
#在输入x中,句子长度不足maxlength的部分都被填上了0.
        self.p = tf.placeholder("float", [batch_size])

# RNN output node weights and biases
#这两个是需要被训练的变量.除此之外,lstm状态也是需要保存的变量.
        self.weights = tf.Variable(tf.random_normal([512, vocab_size])) 
        self.biases =  tf.Variable(tf.random_normal([vocab_size])) 

#在这里定义rnn网络.
        def RNN(x, p, weights, biases):

#rnn为三层,每层节点数分别为1024,512,256.可以任意修改层数和每层节点数,但是修改最后一个256需要把文件里所有的256都替换一下.
            rnn_cell = rnn.MultiRNNCell([rnn.BasicLSTMCell(1024),rnn.BasicLSTMCell(1024),rnn.BasicLSTMCell(512)])

#rnn的初始化状态.
            initial_state = rnn_cell.zero_state(batch_size, dtype=tf.float32)

#这里用的dynamic_rnn可以不像static_rnn一样把maxlength层rnn直接创建出来,
#而是只创建一次并且利用内部自带的"变量"自动叠加.
            outputs, states = tf.nn.dynamic_rnn(rnn_cell, x, sequence_length=p, initial_state=initial_state, dtype=tf.float32)

#outputs的形状为[batch_size,maxlength,256]
#对pad以后的数据,outputs全为0.下面我们抽取那些全为0之前的最后一个输出.
            index = tf.range(0, batch_size, dtype=tf.int32) * maxlength
#index:一个形状为[batch_size]的tensor,为[0,maxlength,maxlength*2,maxlength*3...]
            index=tf.add(index , tf.cast((p - 1),tf.int32))

#这样index变为(如果把outputs的前两维放在一起)每一个序列最后的位置.
#gather:取出第index个行放在一起
#就取到了[batch_size,256]形状的最后输出.
            outputs = tf.gather(tf.reshape(outputs, [-1, 512]), index)

#全联通层.之前的weights和biases两个变量的唯一用处.
            return tf.matmul(outputs, weights) + biases

#构造RNN,取出它的输出:
        self.pred = RNN(self.x, self.p, self.weights, self.biases)

# Loss函数:
        self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.pred, labels=self.y))
# 优化器:
        self.optimizer = tf.train.RMSPropOptimizer(learning_rate=self.learning_rate).minimize(self.cost)
# 预测正确率:(这个与训练无关,纯粹是监控使用)
        self.correct_pred = tf.equal(tf.argmax(self.pred,1), tf.argmax(self.y,1))
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_pred, tf.float32))

if __name__ == '__main__':
	model = rnnmodel()
