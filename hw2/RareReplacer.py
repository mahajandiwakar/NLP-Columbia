#! /usr/bin/python

import json
import sys

class CountReplace:
    def __init__(self):
        self.counts = {}

    def count(self, tree):
        """
        Count the frequencies of terminals in the tree.
        :rtype : object
        """
        if isinstance(tree, basestring):
            return
        if len(tree) == 2:
            # It is a unary rule.
            key = (tree[0], tree[1])
            self.counts.setdefault(key, 0)
            self.counts[key] += 1
        elif len(tree) == 3:
            # Recursively count the children.
            self.count(tree[1])
            self.count(tree[2])

    def replaceRare(self, tree):
        """
        replace all the words that have a count < 5 with rare
        """
        if isinstance(tree, basestring):
            return

        if len(tree) == 2:
            # It is a unary rule.
            key = (tree[0],tree[1])
            val = self.counts.get(key)
            if val < 5:
                tree[1]='_RARE_'
        elif len(tree) == 3:
            # Recursively replace the children.
            self.replaceRare(tree[1])
            self.replaceRare(tree[2])
        return tree

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print 'usage: python RareReplacer.py <Input_File> <Output_File>'
        sys.exit(2)
    replacer = CountReplace()
    parse_file = sys.argv[1]
    write_file = open(sys.argv[2], 'w')
    write_file.truncate()
    for l in open(parse_file):
        t = json.loads(l)
        replacer.count(t)
    for l in open(parse_file):
        t = json.loads(l)
        t = replacer.replaceRare(t)
        write_file.write(json.dumps(t))
        write_file.write('\n')
    write_file.flush()
    write_file.close()








