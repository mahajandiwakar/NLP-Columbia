#!/usr/bin/env python

from IBM_Model2 import IBM2
import math
import sys

class UnScramble():

    def __init__(self, model_tval, model_qval):
        model = IBM2(None, None, None, model_tval, model_qval)
        self.tval = model.tVal
        self.qval = model.qVal

    def unscramble(self, scrambled_en, original_de, writeTo):
        german_iter = open(original_de, 'r')
        writer = open(writeTo, 'w')
        for de_line in german_iter:
            max_score = -10000000000000
            bestSent = ''
            english_iter = open(scrambled_en, 'r')
            for en_line in english_iter:
                score = self.get_score(en_line.strip(),de_line.strip())
                if score > max_score:
                    max_score = score
                    bestSent = en_line
            writer.write(bestSent)
            english_iter.close()
        german_iter.close()
        writer.close()

    def get_score(self, en_sen, de_sen):
        en_words = ['NULL']
        en_words.extend(en_sen.strip().split())
        de_words = de_sen.strip().split()
        m = len(de_words)
        l = len(en_words)-1
        prob = 0
        for i in range(0, m):
            maxVal = 0
            for j in range(0, l+1):
                qvalue = self.qval.get((j, i+1, l, m))
                tvalueDict = self.tval.get(en_words[j])
                if qvalue is None or tvalueDict is None:
                    tempval = 0
                else:
                    tvalue = tvalueDict.get(de_words[i])
                    if tvalue is None:
                        tempval = 0
                    else:
                        tempval = qvalue * tvalue
                        if tempval > maxVal:
                            maxVal = tempval
            if maxVal == 0:
                prob += -100000000
            else:
                prob += math.log(maxVal)
        return prob


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "two inputs required : [tvalmodel] [qvalmodel] [original_foreign] [scrambled_english] "
        sys.exit(2)
    unscrambler = UnScramble(sys.argv[1], sys.argv[2])
    unscrambler.unscramble(sys.argv[4], sys.argv[3], 'unscrambled.en')
