import numpy as np, tensorflow as tf
import os
import itertools
from functools import reduce
import random

class txtdatareader():
    def __init__(self, fileloc,trainratio):
        self.traindataset, self.testdataset = self.readdata(fileloc,trainratio)
        self.trainsize = len(self.traindataset)
        self.testsize  = len(self.testdataset)
        self.maxlen    = 369
        self.minlen    = 369
        self.cursor    = 0
        self.testcursor = 0
        self.trainepochs    = 0
        self.testepochs     = 0

    def get_all_name(self, location):
        datasetlist = os.listdir(location)
        #datasetlist.sort()
        return datasetlist


    def readdata(self,fileloc,trainratio):
        samplelist = self.get_all_name(fileloc)
        print("samplelist",samplelist)
        trainset = []
        testset  = []
        for sample in samplelist:
            dataset = []
            maxfeature = [-float("inf")]*369
            minfeature = [float("inf")]*369
            with open(fileloc+'features.txt', 'r') as readfile:
                for line in readfile:
                    getdata = line.strip('\n').split(',')
                    getdata = list(map(lambda x:float(x),getdata[:-1]))
                    for i in range(len(getdata)):
                        maxfeature[i] = max(maxfeature[i], getdata[i])
                        minfeature[i] = min(minfeature[i], getdata[i])
            try:
                with open(fileloc+'features.txt', 'r') as readfile:
                    for line in readfile:
                        data = line.strip('\n').split(',')
                        temp = []
                        rawsdata = list(map(lambda x:float(x),data[:-1]))
                        for i in range(len(rawsdata)):
                            rawsdata[i] = int(round((rawsdata[i] - minfeature[i]) / (maxfeature[i] - minfeature[i]),2)*100)
                        if data[-1]=='Yes':
                            temp.append([rawsdata,1])
                        else:
                            temp.append([rawsdata,0])
                        dataset += temp
                    print("file:",sample,"  samples:", len(dataset))
            except:
                print("sample %s is not found"%sample)
            trainset += dataset[:int(len(dataset)*trainratio)]
            testset  += dataset[int(len(dataset)*trainratio):]
        return trainset, testset


    def padding(self,array):
        array = np.lib.pad(array, (self.maxlen-len(array),0), 'constant', constant_values=(0))
        return array


    def shuffle(self,Type = "train"):
        if Type == "train":
            random.shuffle(self.traindataset)
        else:
            random.shuffle(self.testdataset)
        self.cursor = 0
        self.testcursor = 0 


    def next_one(self, n,Type = "train"):
        if Type == "train":
            trainlen = len(self.traindataset)
            if self.cursor+n > self.trainsize:
                self.trainepochs += 1
                self.shuffle(Type)
            data = self.traindataset[self.cursor:self.cursor+1][0][0]
            label = self.traindataset[self.cursor:self.cursor+1][0][1]
            self.cursor += n
            slen = 369
            return np.array(data).reshape(1,369), np.array(label).reshape(n), np.array(slen).reshape(1)
        else:
            testlen = len(self.testdataset)
            if self.testcursor+n > self.testsize:
                self.testepochs += 1
                self.shuffle(Type)
            data = self.testdataset[self.testcursor:self.testcursor+1][0][0]
            label = self.testdataset[self.testcursor:self.testcursor+1][0][1]
            self.testcursor += n
            slen = 369
            return np.array(data).reshape(1,369), np.array(label).reshape(n), np.array(slen).reshape(1)

    def next_batch(self, n,Type = "train"):
        Rdata, Rlabel, Rslen = self.next_one(1,Type)
        for i in range(n-1):
            data, label, slen = self.next_one(1,Type)
            Rdata = np.concatenate((Rdata, data), axis=0)
            Rlabel = np.concatenate((Rlabel, label), axis=0)
            Rslen = np.concatenate((Rslen, slen), axis=0)
        return Rdata, Rlabel, Rslen
if __name__ == '__main__':
    test = txtdatareader("../data/",trainratio=0.8)
    maxlen = [3,3,3,3]
    minlen = [1,1,1,1]
    data, label, slen = test.next_batch(3, Type = "train")
    print(slen)

