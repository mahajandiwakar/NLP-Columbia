import sys
import subprocess
from collections import defaultdict
from subprocess import PIPE

def features_set(word, tag, features):
    features.extend(['SUFFIX:' + word[-3:] + ':3:' + tag, 'SUFFIX:' + word[-2:] + ':2:' + tag, 'SUFFIX:' + word[-1:] + ':1:' + tag])
    return features

def call(process, stdin):
    output = process.stdin.write(stdin + '\n\n')
    line = ''
    while 1:
        l = process.stdout.readline()
        if not l.strip():
            break
        line += l
    return line

def get_features(histories, sentence, model, score):
    result = ''
    for history in histories:
        history_list = history.split()
        if len(history_list) > 0 and history_list[2] != 'STOP':
            pos = int(history_list[0]) - 1
            word = sentence[pos].split()[0]
            tag = history_list[2]

            weight = 0
            bigram = 'BIGRAM:' + history_list[1] + ':' + tag
            t = 'TAG:' + word + ':' + tag
            features = features_set(word, tag, [bigram, t])
            for feature in features:
                if score == 1:
                    if feature in model:
                        weight += model[feature]
                else:
                    if feature in model:
                        model[feature] += 1
                    else:
                        model[feature] = 1
            result += (history + ' ' + str(weight) + '\n')
    if score == 1:
        return result[:-1]
    return model

def train_model(train_file, model_file):
    gold_server = subprocess.Popen(['python', 'tagger_history_generator.py', 'GOLD'], stdin=PIPE, stdout=PIPE)
    enum_server = subprocess.Popen(['python', 'tagger_history_generator.py', 'ENUM'], stdin=PIPE, stdout=PIPE)
    history_server = subprocess.Popen(['python', 'tagger_decoder.py', 'HISTORY'], stdin=PIPE, stdout=PIPE)

    model = defaultdict(int)
    gold_dict = {}
    gold_tags = {}
    for it in range(0, 5):
        i = 0
        train_infile = open(train_file, 'r')
        sentence = ''
        for line in train_infile:
            if len(line) > 1:
                sentence += line
            else:
                sentence = sentence[:-1]
                if it == 0:
                    gold = call(gold_server, sentence)
                    gold_tags[i] = gold
                    gold_dict[i] = get_features(gold.split('\n'), sentence.split('\n'), {}, 0)
                histories = call(enum_server, sentence).split('\n')
                scores = get_features(histories, sentence.split('\n'), model, 1)
                tags = call(history_server, scores).split('\n')
                if tags != gold_tags[i]:
                    features = get_features(tags, sentence.split('\n'), {}, 0)
                    for feature in (gold_dict[i]).iterkeys():
                        model[feature] += gold_dict[i][feature]
                    for feature in features.iterkeys():
                        model[feature] -= features[feature]
                i += 1
                sentence = ''
        train_infile.close()
    outfile = open(model_file, 'w')
    for feature in model.iterkeys():
        outfile.write(feature + ' ' + str(model[feature]) + '\n')
    outfile.close()
    return model

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "python q5.py [train_file] [output_file]"
        sys.exit(2)
    train_model(sys.argv[1], sys.argv[2])
