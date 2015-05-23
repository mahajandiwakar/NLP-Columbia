import sys
import subprocess
from collections import defaultdict
from subprocess import PIPE

def assign_tags(model, input_file, output_file):
    enum_server = subprocess.Popen(['python', 'tagger_history_generator.py', 'ENUM'], stdin=PIPE, stdout=PIPE)
    history_server = subprocess.Popen(['python', 'tagger_decoder.py', 'HISTORY'], stdin=PIPE, stdout=PIPE)
    untag_infile = open(input_file, 'r')
    outfile = open(output_file, 'w')
    sentence = ''
    for line in untag_infile:
        if len(line) > 1:
            sentence += line
        else:
            sentence = sentence[:-1]
            histories = call(enum_server, sentence).split('\n')
            sentence = sentence.split()
            scores = get_features(histories, sentence, model)
            tags = call(history_server, scores).split('\n')

            for i in range(0, len(sentence)):
                parsed = tags[i].split()
                outfile.write(sentence[i] + ' ' + parsed[2] + '\n')
            outfile.write('\n')
            sentence = ''
    untag_infile.close()
    outfile.close()

def call(process, stdin):
    output = process.stdin.write(stdin + '\n\n')
    line = ''
    while 1:
        l = process.stdout.readline()
        if not l.strip():
            break
        line += l
    return line

def get_features(histories, sentence, model):
    result = ''
    for history in histories:
        history_list = history.split()
        if history_list and history_list[2] != 'STOP':
            pos = int(history_list[0]) - 1

            word = sentence[pos].split()[0]
            tag = history_list[2]

            weight = 0
            bigram = 'BIGRAM:' + history_list[1] + ':' + tag
            t = 'TAG:' + word + ':' + tag
            features = features_set(word, tag, [bigram, t], sentence, pos)
            for feature in features:
                if feature in model:
                    weight += model[feature]
            result += (history + ' ' + str(weight) + '\n')
    return result[:-1]

def features_set(word, tag, features, sentence, pos):
    features.extend(['SUFFIX:' + word[-3:] + ':3:' + tag, 'SUFFIX:' + word[-2:] + ':2:' + tag, 'SUFFIX:' + word[-1:] + ':1:' + tag])
    features.extend(['PREFIX:' + word[:3] + ':3:' + tag, 'PREFIX:' + word[:2] + ':2:' + tag, 'PREFIX:' + word[:1] + ':1:' + tag])
    features.extend(['SUFFIX:' + word[-4:] + ':4:' + tag])
    features.extend(['PREFIX:' + word[:4] + ':4:' + tag])
    if pos != 0:
        features.extend(['PREVWORD:'+sentence[pos-1].split()[0]+':'+tag])
        features.extend(['PREVBIGRAM:'+sentence[pos-1].split()[0]+':'+word+':'+tag])
    if pos > 1:
        features.extend(['2PREVWORD:'+sentence[pos-2].split()[0]+':'+tag])
        features.extend(['2PREVBIGRAM:'+sentence[pos-2].split()[0]+':'+sentence[pos-1].split()[0]+':'+tag])
    if pos < len(sentence)-1:
        features.extend(['NEXTVWORD:'+sentence[pos+1].split()[0]+':'+tag])
        features.extend(['NEXTBIGRAM:'+word+':'+sentence[pos+1].split()[0]+':'+tag])
    if pos < len(sentence)-2:
        features.extend(['2NEXTVWORD:'+sentence[pos+2].split()[0]+':'+tag])
        features.extend(['2NEXTBIGRAM:'+sentence[pos+1].split()[0]+':'+sentence[pos+2].split()[0]+':'+tag])
    return features


#read the model
def get_model(model_file):
    linefile = open(model_file, 'r')
    model = defaultdict(int)
    for line in linefile:
        line_list = line.split()
        model[line_list[0]] = float(line_list[1])
    linefile.close()
    return model


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "python q4.py [model_file] [untagged_file] [output_file]"
        sys.exit(2)
    model = get_model(sys.argv[1])
    assign_tags(model, sys.argv[2], sys.argv[3])
