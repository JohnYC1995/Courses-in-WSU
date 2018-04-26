import os
import re
import numpy as np
from sklearn.preprocessing import scale
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
import io
import json
def read_data(loc):
    data_list = []
    label_list = []
    #os.walk is a generator
    for root, _, files in os.walk(loc):
        pass
    for name in files:
        readf = open(os.path.join(root, name),'r',encoding="utf-8")
        for line in readf:
            data_list.append(list(eval(line))[1:-1])
            label_list.append(list(eval(line))[-1:])
    return np.array(data_list), np.array(label_list).reshape(len(label_list),)


def load_data(loc):
    data_list = []
    readf = open(loc,'r',encoding="utf-8")
    for line in readf:
        data_list.append(list(map(eval,line.strip().split())))
    return np.array(data_list)


def read_data2(loc1, loc2):
    data_list = load_data(loc1)
    label_list = load_data(loc2)
    return data_list, label_list.reshape(len(label_list),)


def read_data3(loc):
    data_list = []
    label_list = []
    #os.walk is a generator
    for root, _, files in os.walk(loc):
        pass
    for name in files:
        readf = open(os.path.join(root, name),'r',encoding="utf-8")
        for line in readf:
            line = list(map(lambda x: 0 if x=='NaN' else x,line.split()))
            line = list(map(float,line))
            data_list.append(line[2:-1])
            label_list.append(line[1:2])
    return np.array(data_list), np.array(label_list).reshape(len(label_list),)

def read_data4(loc):
    pass
if __name__ == '__main__':
    dataloc = '../UCIHAR/train/X_train.txt'
    labelloc = '../UCIHAR/train/y_train.txt'
    loc = '../PAMAP2_Dataset/Protocol/'
    dpath = loc + 'data.json'
    lpath = loc + 'label.json'
    data, label= read_data3(loc)
    #print(len(label))
    with open(dpath, 'w') as write_file:
        json.dump(data.tolist(), write_file, indent = 4)
    with open(lpath, 'w') as write_file:
        json.dump(label.tolist(), write_file, indent = 4)
    with open(dpath, 'r') as read_file:
        data1 = json.load(read_file)
    with open(lpath, 'r') as read_file:
        label1 = json.load(read_file)
    print(label1)
    np.set_printoptions(threshold=1000000)
    #print(label)