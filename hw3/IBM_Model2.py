#!/usr/bin/env python

from collections import defaultdict
from IBM_Model1 import IBM1
import pickle
import sys
import gzip

class IBM2():
    def __init__(self, corpus_en, corpus_de, iterations=5, filenameTVal=None, filenameQVal=None):
        self.english_file = corpus_en
        self.german_file = corpus_de
        self.iterations = iterations
        self.qVal = defaultdict(float)

        #intialize t(f|e) = using IBM Model 1
        if filenameTVal is None:
            model = IBM1(self.english_file, self.german_file)
            model.expMax()
            self.tVal = model.tVal
        else:
            self.readModelFromFile(filenameTVal, filenameQVal)

        if filenameQVal is None:
            #intialize q(j|i,l,m) = 1/l+1
            english_iter = open(corpus_en, 'r')
            german_iter = open(corpus_de, 'r')
            for de_line in german_iter:
                l = len(english_iter.readline().strip().split())
                m = len(de_line.strip().split())
                for i in range(0, m):
                    for j in range(0, l+1):
                        self.qVal[(j, i+1, l, m)] = 1.0/float(l+1)
            english_iter.close()
            german_iter.close()


    #Expectation Maximization Algorithm
    def expMax(self):
        for iter in range(0, self.iterations):
            english_iter = open(self.english_file, 'r')
            german_iter = open(self.german_file, 'r')
            counts = defaultdict(float)
            for de_line in german_iter:
                en_words = ['NULL']
                en_words.extend(english_iter.readline().strip().split())
                de_words = de_line.strip().split()
                m = len(de_words)
                en_len = len(en_words)
                l = en_len-1
                for i in range(0, m):
                    delta_denom = 0
                    delta_num = []
                    for j in range(0, en_len):
                        tempval = self.qVal[(j, i+1, l, m)] * self.tVal[en_words[j]][de_words[i]]
                        delta_denom += tempval
                        delta_num.append(tempval)
                    for j in range(0, en_len):
                        if delta_num[j] > 0:
                            en_word = en_words[j]
                            tempval = float(delta_num[j])/float(delta_denom)
                            counts[(en_word, de_words[i])] += tempval
                            counts[en_word] += tempval
                            #l,m,i,j
                            counts[(j, i+1, l, m)] += tempval
                            counts[(i+1, l, m)] += tempval

            #updating tVals
            for en_word in self.tVal.iterkeys():
                for key, value in (self.tVal.get(en_word).iteritems()):
                    self.tVal[en_word][key] = float(counts[(en_word, key)])/float(counts[en_word])
            #updating qVals
            for j, i, l, m in self.qVal.iterkeys():
                self.qVal[(j, i, l, m)] = float(counts[(j, i, l, m)]) / counts[(i, l, m)]
            english_iter.close()
            german_iter.close()


    def align(self, en_sentence, de_sentence):
        en_words = ['NULL']
        en_words.extend(en_sentence.strip().split())
        de_words = de_sentence.strip().split()
        l = len(en_words)-1
        m = len(de_words)
        alignarray = []
        for i in range(0, m):
            maxVal = 0
            align = -1
            for j in range(0, l+1):
                tempval = self.qVal[(j, i+1, l, m)] * self.tVal[en_words[j]][de_words[i]]
                if tempval > maxVal:
                    maxVal = tempval
                    align = j
            alignarray.append(align)
        return alignarray

    def writeModelToFile(self, filenameQVal, filenameTVal=None):
        with open(filenameQVal + '.pkl', 'wb') as f:
            pickle.dump(self.qVal, f, pickle.HIGHEST_PROTOCOL)

        if filenameTVal is not None:
            with open(filenameTVal + '.pkl', 'wb') as f:
                pickle.dump(self.tVal, f, pickle.HIGHEST_PROTOCOL)


    def readModelFromFile(self, filenameTVal, filenameQVal=None):
        with open(filenameTVal + '.pkl', 'rb') as f:
            self.tVal = pickle.load(f)
        if filenameQVal is not None:
            with open(filenameQVal + '.pkl', 'rb') as f:
                self.qVal = pickle.load(f)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Two inputs required : [english_corpus_compressed] [german_corpus_compressed]"
        sys.exit(2)
    with gzip.open(sys.argv[1], 'rb') as infile:
        with open('corpus.en', 'w') as outfile:
            for line in infile:
                outfile.write(line)
    with gzip.open(sys.argv[2], 'rb') as infile:
        with open('corpus.de', 'w') as outfile:
            for line in infile:
                outfile.write(line)
    if len(sys.argv) == 3:
        model = IBM2('corpus.en', 'corpus.de', 5)
    else:
        model = IBM2('corpus.en', 'corpus.de', 5, sys.argv[3])
    model.expMax()
    english_iter = open('corpus.en', 'r')
    german_iter = open('corpus.de', 'r')
    print 'Aligments for 20 sentences in the training Data'
    for i in range(0, 20):
        de_line = german_iter.readline()
        en_line = english_iter.readline()
        print 'English:' + en_line,
        print 'German:' + de_line,
        print 'Alignment:',
        print model.align(en_line, de_line)
        print
    english_iter.close()
    german_iter.close()
    model.writeModelToFile('qvalModel')

