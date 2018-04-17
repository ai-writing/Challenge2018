#-*- coding:utf-8 -*-
#n51.py 
#learning rate decay
#patchlength 0 readfrom resp
#add:saving session

import numpy as np
import tensorflow as tf
import time
import os
from attnmodel import BiRNN
from reader import reader

# Parameters
# =================================================
tf.flags.DEFINE_integer('embedding_size', 100, 'embedding dimension of tokens')
tf.flags.DEFINE_integer('rnn_size', 20, 'hidden units of RNN , as well as dimensionality of character embedding (default: 100)')
#tf.flags.DEFINE_integer('rnn_size', 100, 'hidden units of RNN , as well as dimensionality of character embedding (default: 100)')
tf.flags.DEFINE_float('dropout_keep_prob', 0.5, 'Dropout keep probability (default : 0.5)')#too high?
tf.flags.DEFINE_integer('layer_size', 2, 'number of layers of RNN (default: 2)')
tf.flags.DEFINE_integer('batch_size', 50, 'Batch Size (default : 32)')
#tf.flags.DEFINE_integer('sequence_length', 15, 'Sequence length (default : 32)')
tf.flags.DEFINE_integer('attn_size', 1024, 'attention layer size')
tf.flags.DEFINE_float('grad_clip', 5.0, 'clip gradients at this value')
tf.flags.DEFINE_integer("num_epochs", 300, 'Number of training epochs (default: 200)')
tf.flags.DEFINE_float('learning_rate', 0.00005, 'learning rate')
tf.flags.DEFINE_string('train_file', 'rt_train.txt', 'train raw file')
tf.flags.DEFINE_string('test_file', 'rt_test.txt', 'train raw file')
tf.flags.DEFINE_string('data_dir', 'data', 'data directory')
tf.flags.DEFINE_string('save_dir', 'ckpt/runattn', 'model saved directory')
tf.flags.DEFINE_string('log_dir', 'log/runattn', 'log info directiory')
tf.flags.DEFINE_string('pre_trained_vec', None, 'using pre trained word embeddings, npy file format')
#tf.flags.DEFINE_string('init_from', 'save', 'continue training from saved model at this path')
tf.flags.DEFINE_string('init_from', None, 'continue training from saved model at this path')
#tf.flags.DEFINE_string('init_from', 'ckpt/runattn', 'continue training from saved model at this path')
#tf.flags.DEFINE_integer('save_steps', 1000, 'num of train steps for saving model')
tf.flags.DEFINE_integer('vocab_size', 1000, 'num of train steps for saving model')
tf.flags.DEFINE_integer('n_classes', 6, 'num of train steps for saving model')
tf.flags.DEFINE_integer('num_batches', 1000000, 'num of train steps for saving model')

FLAGS = tf.flags.FLAGS
#FLAGS._parse_flags()

os.environ["CUDA_VISIBLE_DEVICES"]="1"
embedding_size=100
patchlength=3
num_verbs=1

maxlength=200
#maxlength=15
verbtags=['VB','VBZ','VBP','VBD','VBN','VBG']

global_step = tf.Variable(0, trainable=False)
learning_rate = tf.train.exponential_decay(FLAGS.learning_rate, global_step=global_step, decay_steps=100,decay_rate=0.9)
training_iters = 1000000
display_step = 20

# number of units in RNN cell
n_hidden = 512


start_time = time.time()
def elapsed(sec):
    if sec<60:
        return str(sec) + " sec"
    elif sec<(60*60):
        return str(sec/60) + " min"
    else:
        return str(sec/(60*60)) + " hr"

def getMem(aa):
    with open('/proc/meminfo') as f:
        total = int(f.readline().split()[1])
        free = int(f.readline().split()[1])
        buffers = int(f.readline().split()[1])
        cache = int(f.readline().split()[1])
        while buffers<10000000:
            print('wait',buffers,aa)
            time.sleep(60)
            buffers = int(f.readline().split()[1])


# Target log path
logs_path = 'log/rnn_words'
writer = tf.summary.FileWriter(logs_path)


data=reader(patchlength=patchlength,\
            maxlength=maxlength,\
            embedding_size=embedding_size,\
            num_verbs=num_verbs,\
            shorten=True,\
            shorten_front=True)  


def main(_):

    '''
    test_data_loader = InputHelper()
    test_data_loader.load_dictionary(FLAGS.data_dir+'/dictionary')
    test_data_loader.create_batches(FLAGS.data_dir+'/'+FLAGS.test_file, 100, maxlength)
    '''
    if FLAGS.pre_trained_vec:
        embeddings = np.load(FLAGS.pre_trained_vec)
        print(embeddings.shape)
        FLAGS.vocab_size = embeddings.shape[0]
        FLAGS.embedding_size = embeddings.shape[1]

    if FLAGS.init_from is not None:
        assert os.path.isdir(FLAGS.init_from), '{} must be a directory'.format(FLAGS.init_from)
        ckpt = tf.train.get_checkpoint_state(FLAGS.init_from)
        assert ckpt,'No checkpoint found'
        assert ckpt.model_checkpoint_path,'No model path found in checkpoint'

    # Define specified Model
    model = BiRNN(embedding_size=FLAGS.embedding_size, rnn_size=FLAGS.rnn_size, layer_size=FLAGS.layer_size,    
        vocab_size=FLAGS.vocab_size, attn_size=FLAGS.attn_size, sequence_length=maxlength,
        n_classes=FLAGS.n_classes, grad_clip=FLAGS.grad_clip, learning_rate=FLAGS.learning_rate)

    # define value for tensorboard
    tf.summary.scalar('train_loss', model.cost)
    tf.summary.scalar('accuracy', model.accuracy)
    merged = tf.summary.merge_all()

    # 调整GPU内存分配方案
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.per_process_gpu_memory_fraction=0.4#占用40%显存
#    tf_config.gpu_options.allow_growth = True

    
    max_acc=0

    with tf.Session(config=tf_config) as sess:
        train_writer = tf.summary.FileWriter(FLAGS.log_dir, sess.graph)

        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver(tf.global_variables())

        # using pre trained embeddings
        if FLAGS.pre_trained_vec:
            sess.run(model.embedding.assign(embeddings))
            del embeddings

        # restore model
        if FLAGS.init_from is not None:
            saver.restore(sess, ckpt.model_checkpoint_path)


        sess.graph.finalize() 
        start = time.time()


        print('start')
        total_loss=0
        total_acc=0
        for e in range(FLAGS.num_batches):
            inputs,pads,answers,_ = data.list_tags(FLAGS.batch_size)
            getMem(0)
            feed = {model.input_data:inputs, model.targets:answers, model.output_keep_prob:FLAGS.dropout_keep_prob,model.pad:pads}
            getMem(1)
            train_loss,acc, summary,  _ = sess.run([model.cost,model.accuracy, merged, model.train_op], feed_dict=feed)
            total_loss+=train_loss
            total_acc+=acc


            
            if e % 100 == 0:
                print('{}/{} , train_loss = {}, accuracy= {}, time/batch = {}'.format(e, FLAGS.num_batches,  total_loss/100, total_acc/100, time.time()-start))
                start = time.time()
                total_loss=0
                total_acc=0


            if e % 100 == 0:
                train_writer.add_summary(summary, e)

            if e % 500 == 0:
                checkpoint_path = os.path.join(FLAGS.save_dir, 'model.ckpt')        
                saver.save(sess, checkpoint_path, global_step=e)
                print('model saved to {}'.format(checkpoint_path))

            '''
            print ' loss:',total_loss/FLAGS.num_batches
            test_data_loader.reset_batch()
            test_accuracy = []
            for i in range(test_data_loader.num_batches):
                test_x, test_y = test_data_loader.next_batch()
                feed = {model.input_data:test_x, model.targets:test_y, model.output_keep_prob:1.0}
                accuracy = sess.run(model.accuracy, feed_dict=feed)
                test_accuracy.append(accuracy)
            print 'test accuracy:{0}'.format(np.average(test_accuracy)),' loss:',total_loss/FLAGS.num_batches
            '''

if __name__ == '__main__':
    tf.app.run()
