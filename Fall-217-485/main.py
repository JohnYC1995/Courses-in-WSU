from Network import RNNforclassfication
import tensorflow as tf
import os

def configure():
	flags = tf.app.flags
	#experiments steup
	flags.DEFINE_integer('max_epoch',100,'# of step in an epoch')
	flags.DEFINE_integer('test_step',1,'# of step to test a model')
	flags.DEFINE_float('learning_rate',1e-4,'learning rate')
	flags.DEFINE_integer('save_step',5,'# of step to save a model')
	flags.DEFINE_string('logdir', './logdir', 'log directory')
	#data informattion
	flags.DEFINE_string('dataset_dir','../data/','whole dataset directory')
	flags.DEFINE_integer('traindataratio',0.001,'sperate whole data into train and test by the ratio')
	#network
	flags.DEFINE_integer('batch',1, '# batch size')
	flags.DEFINE_integer('vocab_size',101, 'vocab size')
	flags.DEFINE_integer('state_size', 40, 'state size')
	flags.DEFINE_integer('num_classes',2, 'total classes')
	#Models
	flags.DEFINE_string('rnntype','LSTM','choose LSTM  or GRU cell')
	flags.DEFINE_integer('num_layers', 2, '# OF LSTM layers')
	flags.FLAGS.__dict__['__parsed'] = False
	return flags.FLAGS

if __name__ == '__main__':
    os.environ['CUDA_VISIBLE_DEVICES'] = '6'
    conf = configure()
    RNN = RNNforclassfication(conf)
    g = RNN.RNNnetwork()
    tr_losses, te_losses = RNN.train(g)
