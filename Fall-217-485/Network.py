import tensorflow as tf, numpy as np
import os
from datareader import txtdatareader

class RNNforclassfication(object):
    def __init__(self, conf):
        self.reset_graph()
        self.conf = conf
        self.writer = tf.summary.FileWriter(self.conf.logdir)

    def reset_graph(self):
        if 'sess' in globals() and sess:
            sess.close()
        tf.reset_default_graph()

    def save_summary(self, summary, step):
        print('---->summarizing', step)
        self.writer.add_summary(summary, step)

    def RNNnetwork(self):
        # Placeholders
        x = tf.placeholder(tf.int32, [self.conf.batch, None]) # [batch_size, num_steps]
        seqlen = tf.placeholder(tf.int32, [self.conf.batch])
        y = tf.placeholder(tf.int32, [self.conf.batch])
        keep_prob = tf.placeholder_with_default(1.0, [])
        # Embedding layer
        embeddings = tf.get_variable('embedding_matrix', [self.conf.vocab_size, self.conf.state_size])
        rnn_inputs = tf.nn.embedding_lookup(embeddings, x)
        
        # RNN
        print("Model type:",self.conf.rnntype)
        if self.conf.rnntype == "GRU":
            cell = tf.nn.rnn_cell.GRUCell(self.conf.state_size)
            init_state = tf.get_variable('init_state', [1, self.conf.state_size],\
                initializer=tf.constant_initializer(0.0))
            init_state = tf.tile(init_state, [self.conf.batch, 1])
        elif self.conf.rnntype == 'LSTM':
            cell = tf.nn.rnn_cell.LSTMCell(num_units=self.conf.state_size,state_is_tuple=True)
            cell = tf.nn.rnn_cell.MultiRNNCell(cells=[cell]*self.conf.num_layers, state_is_tuple=True)
            init_state = cell.zero_state(self.conf.batch, dtype=tf.float32)
        else:
            print('the model does not exist!')
            return
        rnn_outputs, final_state = tf.nn.dynamic_rnn(cell = cell, inputs=rnn_inputs, sequence_length=seqlen,
                                                     initial_state=init_state)
        # Add dropout, as the model otherwise quickly overfits
        rnn_outputs = tf.nn.dropout(rnn_outputs, keep_prob)
        idx = tf.range(self.conf.batch)*tf.shape(rnn_outputs)[1] + (seqlen - 1)
        last_rnn_output = tf.gather(tf.reshape(rnn_outputs, [-1, self.conf.state_size]), idx)
       
        # Softmax layer
        with tf.variable_scope('softmax'):
            W = tf.get_variable('W', [self.conf.state_size, self.conf.num_classes])
            b = tf.get_variable('b', [self.conf.num_classes], initializer=tf.constant_initializer(0.0))
        logits = tf.matmul(last_rnn_output, W) + b
        preds = tf.nn.softmax(logits)
        correct = tf.equal(tf.cast(tf.argmax(preds,1),tf.int32), y)
        self.accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
        self.loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=y))
        train_step = tf.train.AdamOptimizer(self.conf.learning_rate).minimize(self.loss)
        return {'x': x,'y': y,'seqlen':seqlen,'dropout': keep_prob,'loss': self.loss,\
                'ts': train_step,'preds': preds,'accuracy': self.accuracy}

    def config_summary(self, name):
        summarys = []
        summarys.append(tf.summary.scalar(name+'/loss', self.loss))
        summarys.append(tf.summary.scalar(name+'/accuracy', self.accuracy))
        summary = tf.summary.merge(summarys)
        return summary

    def save_summary(self, summary, step):
        print('---->summarizing', step)
        self.writer.add_summary(summary)

    def train(self,graph):
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            self.writer.add_graph(sess.graph)
            datareader = txtdatareader(self.conf.dataset_dir, self.conf.traindataratio)
            step, accuracy, loss = 0, 0, 0
            tr_accuracy, te_accuracy = [], []
            tr_loss, te_loss = [], []
            current_epoch = 0
            while current_epoch < self.conf.max_epoch:
                step += 1
                data, label,slen = datareader.next_batch(self.conf.batch,Type="train")
                feed = {graph['x']: data, graph['y']: label,graph['seqlen']:slen, graph['dropout']: 0.6}
                accuracy_,loss_, _, summary = sess.run([graph['accuracy'], graph['loss'], graph['ts'],\
                                        self.config_summary('train')], feed_dict=feed)
                #self.save_summary(summary, step)
                accuracy += accuracy_
                loss     += loss_
                #print("iterations%d correct num%d\n"%(step,accuracy),accuracy/ (step))
                if datareader.trainepochs > current_epoch:
                    current_epoch += 1
                    tr_accuracy.append(accuracy / step)
                    tr_loss.append(loss / step)
                    step, accuracy,loss = 0, 0, 0
                    #eval test set
                    te_epoch = datareader.testepochs
                    while datareader.testepochs == te_epoch and step<18:
                        step += 1
                        data, label,slen = datareader.next_batch(self.conf.batch,Type="test")
                        feed = {graph['x']: data, graph['y']: label,graph['seqlen']:slen, graph['dropout']: 0.6}
                        accuracy_,loss_,summary = sess.run([graph['accuracy'],graph['loss'],\
                            self.config_summary('test')], feed_dict=feed)
                        self.save_summary(summary,step)
                        accuracy += accuracy_
                        loss   += loss_
                    te_accuracy.append(accuracy / step)
                    te_loss.append(loss / step)
                    step, accuracy, loss = 0,0,0
                    print("Accuracy after epoch", current_epoch, \
                          " - tr accuracy:", tr_accuracy[-1], "loss:",tr_loss[-1],\
                          "- te accuracy:", te_accuracy[-1],"loss:",te_loss[-1])
        return tr_accuracy, te_accuracy


if __name__ == '__main__':
    pass