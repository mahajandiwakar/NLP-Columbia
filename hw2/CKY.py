#!/usr/bin/env python

import sys
import json
from collections import defaultdict



def read_counts(counts_file):
    fi = open(counts_file, 'r')
    for line in fi:
        fields = line.strip().split(' ')
        yield fields


class CKY():
    def __init__(self):
        self.nonterminal_counts = defaultdict(int)
        self.binary_rule_counts = defaultdict(int)
        self.unary_rule_counts = defaultdict(int)

    def train(self, counts_file):
        for l in read_counts(counts_file):
            n, count_type, args = int(l[0]), l[1], l[2:]
            if count_type == 'NONTERMINAL':
                self.nonterminal_counts[args[0]] = n
            elif count_type == 'BINARYRULE':
                self.binary_rule_counts[tuple(args)] = n
            else:
                self.unary_rule_counts[tuple(args)] = n

    def q(self, x, y1, y2):
        return float(self.binary_rule_counts[x, y1, y2]) / self.nonterminal_counts[x]

    def q_unary(self, x, w):
        return float(self.unary_rule_counts[x, w]) / self.nonterminal_counts[x]


    def CKY(self, x):
        n = len(x)
        pi = defaultdict(float)
        bp = {}
        N = self.nonterminal_counts.keys()
        for i in xrange(n):
            if sum([self.unary_rule_counts[X, x[i]] for X in N]) < 5:
                w = '_RARE_'
            else:
                w = x[i]
            for X in N:
                pi[i, i, X] = self.q_unary(X, w)

        for l in xrange(1, n):
            for i in xrange(n-l):
                j = i + l
                for X in N:
                    max_score = 0
                    args = None
                    for R in self.binary_rule_counts.keys():
                        if R[0] == X:
                            Y, Z = R[1:]
                            for s in xrange(i, j):
                                if pi[i, s, Y] and pi[s + 1, j, Z]:
                                    score = self.q(X, Y, Z) * pi[i, s, Y] * pi[s + 1, j, Z]
                                    if max_score < score:
                                        max_score = score
                                        args = Y, Z, s
                    if max_score:
                        pi[i, j, X] = max_score
                        bp[i, j, X] = args
        if pi[0, n-1, 'S']:
            return self.recover_tree(x, bp, 0, n-1, 'S')
        else:
            max_score = 0
            args = None
            for X in N:
                if max_score < pi[0, n-1, X]:
                    max_score = pi[0, n-1, X]
                    args = 0, n-1, X
            print json.dumps(self.recover_tree(x, bp, *args))

    def recover_tree(self, x, bp, i, j, X):
        if i == j:
            return [X, x[i]]
        else:
            Y, Z, s = bp[i, j, X]
            return [X, self.recover_tree(x, bp, i, s, Y),
                    self.recover_tree(x, bp, s+1, j, Z)]


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "two inputs required : [counts_file] [input_file]"
        sys.exit(2)
    parser = CKY()
    parser.train(sys.argv[1])
    f = open(sys.argv[2])
    for l in f:
        parser.CKY(l.split(' '))