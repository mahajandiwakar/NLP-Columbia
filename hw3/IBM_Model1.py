#!/usr/bin/env python

import operator
from collections import defaultdict
import pickle
import gzip
import sys

class IBM1():

    def __init__(self, corpus_en=None, corpus_de=None, iterations=5, tvalfile=None):
        if tvalfile is not None:
            self.readModelFromFile(tvalfile)
        else:
            self.english_file = corpus_en
            self.german_file = corpus_de
            self.iterations = iterations
            self.tVal = defaultdict(dict)
            self.german_words = set()
            english_iter = open(corpus_en, 'r')
            german_iter = open(corpus_de, 'r')
            for de_line in german_iter:
                en_words = english_iter.readline().strip().split()
                en_words.append('NULL')
                de_words = de_line.strip().split()
                for enword in en_words:
                    for deword in de_words:
                        self.tVal[enword][deword] = 0
                        self.german_words.add(deword)
            english_iter.close()
            german_iter.close()

            #intialize t(f|e) = 1/n(e)
            for en_word in self.tVal.iterkeys():
                for key, value in (self.tVal.get(en_word).iteritems()):
                    self.tVal[en_word][key] = 1.0/float(len(self.german_words))

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
                de_len = len(de_words)
                en_len = len(en_words)
                for i in range(0, de_len):
                    delta_denom = 0
                    delta_num = []
                    for j in range(0, en_len):
                        tempval = self.tVal[en_words[j]][de_words[i]]
                        delta_denom += tempval
                        delta_num.append(tempval)
                    for j in range(0, en_len):
                        if delta_num[j] > 0:
                            en_word = en_words[j]
                            tempval = float(delta_num[j])/float(delta_denom)
                            counts[(en_word, de_words[i])] += tempval
                            counts[en_word] += tempval
                            #l,m,i,j
                            #counts[en_len][de_len][i][j] += tempval
                            #counts[en_len][de_len][i] += tempval
            for en_word in self.tVal.iterkeys():
                for key, value in (self.tVal.get(en_word).iteritems()):
                    self.tVal[en_word][key] = float(counts[(en_word, key)])/float(counts[en_word])
            english_iter.close()
            german_iter.close()

#Printing top 10 foreign words for the english words
    def getTopWords(self, devwords):
        dev_file = open(devwords, 'r')
        printdevwords = open('devwords_top10.txt', 'w')
        for word in dev_file:
            printdevwords.write('\n\nWord:'+ word)
            en_map = self.tVal.get(word.strip())
            if en_map is not None:
                sorted_ge_list = sorted(en_map.items(), key=operator.itemgetter(1), reverse=True)
                for i in range(0, 10):
                    printdevwords.write(str(sorted_ge_list[i]))

    def align(self, en_sentence, de_sentence):
        en_words = ['NULL']
        en_words.extend(en_sentence.strip().split())
        de_words = de_sentence.strip().split()
        alignarray = []
        for de_word in de_words:
            maxVal = 0
            align = -1
            count = 0
            for en_word in en_words:
                tempval = self.tVal[en_word][de_word]
                if tempval > maxVal:
                    maxVal = tempval
                    align = count
                count +=1
            alignarray.append(align)
        return alignarray

    def writeModelToFile(self, filename):
        with open(filename + '.pkl', 'wb') as f:
            pickle.dump(self.tVal, f, pickle.HIGHEST_PROTOCOL)

    def readModelFromFile(self, filename):
        with open(filename + '.pkl', 'rb') as f:
            self.tVal = pickle.load(f)

if __name__ == '__main__':
    if len(sys.argv) != 3:
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
    model = IBM1('corpus.en', 'corpus.de')
    model.expMax()
    model.getTopWords('devwords.txt')
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
    model.writeModelToFile('tvalModel1')

