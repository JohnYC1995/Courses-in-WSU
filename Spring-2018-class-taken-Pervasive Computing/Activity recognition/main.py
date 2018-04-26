from data_reader import read_data, read_data2, read_data3
from models import *
from sklearn.model_selection import train_test_split
import timeit

if __name__ == '__main__':
	#data preparation
	#location = '../Datasets_Healthy_Older_People/S1_Dataset/'
	dataloc = '../UCIHAR/train/X_train.txt'
	labelloc = '../UCIHAR/train/y_train.txt'
	#loc = '../PAMAP2_Dataset/Protocol/'
	#X, y= read_data(location)
	X, y= read_data2(dataloc, labelloc)
	X = scale(X)
	X_train, X_test, y_train, y_test = \
			train_test_split(X, y, test_size=0.33, random_state=42)

	#LinearSVC kernel = linear
	Model_LinearSVC(X_train, X_test, y_train, y_test)

	#SVC kernel = RBF;gamma = 1 / n_features; decision_function_shape= ovo
	Model_SVC(X_train, X_test, y_train, y_test)

	#decision tree
	Model_decisiontree(X_train, X_test, y_train, y_test)

	#Random Forest
	Model_RandomForest(X_train, X_test, y_train, y_test)

	#NaiveBayes 
	Model_NaiveBayes(X_train, X_test, y_train, y_test)
	#Multi layer perceptron: Fully-connected Neural Network

	Model_MLP(X_train, X_test, y_train, y_test,11,5)

	#Convolutional Neural Networks
