from sklearn.preprocessing import scale
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.ensemble import RandomForestClassifier
import graphviz 
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.metrics import f1_score
import timeit


def Model_LinearSVC(X_train, X_test, y_train, y_test):
	start = timeit.timeit()
	y1 = OneVsOneClassifier(LinearSVC(random_state=0)).fit(X_train, y_train).predict(X_test)
	print("LinearSVC test accuracy: ",accuracy_score(y_test,y1))
	print("LinearSVC test f1: ",f1_score(y1, y_test, average='weighted'))
	end = timeit.timeit()
	print("run time", end -start)
	print("=======================================")


def Model_SVC(X_train, X_test, y_train, y_test):
	start = timeit.timeit()
	y1 = SVC(decision_function_shape='ovo').fit(X_train, y_train).predict(X_test)
	print("SVC with RBF kernel test accuracy: ",accuracy_score(y_test,y1))
	print("SVC with RBF kernel test f1: ",f1_score(y1, y_test, average='weighted'))
	end = timeit.timeit()
	print("run time", end -start)
	print("=======================================")


def Model_decisiontree(X_train, X_test, y_train, y_test):
	start = timeit.timeit()
	clf = tree.DecisionTreeClassifier()
	clf.fit(X_train, y_train)
	y1 = clf.predict(X_test)
	print("decision tree test accuracy: ",accuracy_score(y_test,y1))
	print("decision tree test f1: ",f1_score(y1, y_test, average='weighted'))
	end = timeit.timeit()
	print("run time", end -start)
	print("=======================================")
	#save 
	#dot_data = tree.export_graphviz(clf, out_file=None,
	#					 feature_names =['xAcc','yAcc','zAcc','Id','RSSI',\
	#					 				'Phase','Freq'],
	#					 class_names=['sit on bed', 'sit on chair','lying',\
	#					 				'ambulating',],
    #                     filled=True, rounded=True,  
    #                     special_characters=True)
	#graph = graphviz.Source(dot_data) 
	#graph.render("decision tree results", view =False)


def Model_RandomForest(X_train, X_test, y_train, y_test):
	start = timeit.timeit()
	clf = RandomForestClassifier(n_estimators=10)
	clf.fit(X_train,y_train)
	y1 = clf.predict(X_test)
	print("RandomForest test accuracy: ",accuracy_score(y_test,y1))
	print("RandomForest test f1: ",f1_score(y1, y_test, average='weighted'))
	end = timeit.timeit()
	print("run time", end -start)
	print("=======================================")


def Model_NaiveBayes(X_train, X_test, y_train, y_test):
	start = timeit.timeit()
	model_list = [BernoulliNB(), GaussianNB()]
	model_name = ['BernoulliNB', 'GaussianNB']
	for i, model in enumerate(model_list):
		gnb = model
		y1 = gnb.fit(X_train, y_train).predict(X_test)
		print("NaiveBayes with "+model_name[i]+" test accuracy: ",accuracy_score(y_test,y1))
		print("NaiveBayes with "+model_name[i]+" test f1: ",f1_score(y1, y_test, average='weighted'))
	end = timeit.timeit()
	print("run time", end -start)
	print("=======================================")


def Model_MLP(X_train, X_test, y_train, y_test,ls,ks):
	start = timeit.timeit()
	clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                     hidden_layer_sizes=(ls, ks), random_state=1)
	clf.fit(X_train,y_train)
	y1 = clf.predict(X_test)
	print("Fully-connected network test accuracy: ",accuracy_score(y_test,y1))
	print("Fully-connected network test f1: ",f1_score(y1, y_test, average='weighted'))
	end = timeit.timeit()
	print("run time", end -start)
	print("=======================================")


