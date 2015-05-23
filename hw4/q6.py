import sys
import subprocess
from collections import defaultdict
from subprocess import PIPE

def features_set(word, tag, features, feat, sentence, pos):
    if feat in ['suff','all']:
        features.extend(['SUFFIX:' + word[-3:] + ':3:' + tag, 'SUFFIX:' + word[-2:] + ':2:' + tag, 'SUFFIX:' + word[-1:] + ':1:' + tag])
        features.extend(['SUFFIX:' + word[-4:] + ':4:' + tag])
    if feat in ['prefix', 'suff', 'all']:
        features.extend(['PREFIX:' + word[:3] + ':3:' + tag, 'PREFIX:' + word[:2] + ':2:' + tag, 'PREFIX:' + word[:1] + ':1:' + tag])
        features.extend(['PREFIX:' + word[:4] + ':4:' + tag])
    if feat in ['word', 'all']:
        if pos != 0:
            features.extend(['PREVWORD:'+sentence[pos-1].split()[0]+':'+tag])
        if pos > 1:
            features.extend(['2PREVWORD:'+sentence[pos-2].split()[0]+':'+tag])
        if pos < len(sentence)-1:
            features.extend(['NEXTVWORD:'+sentence[pos+1].split()[0]+':'+tag])
        if pos < len(sentence)-2:
            features.extend(['2NEXTVWORD:'+sentence[pos+2].split()[0]+':'+tag])
    if feat in ['wordsBigrams', 'all']:
        if pos != 0:
            features.extend(['PREVBIGRAM:'+sentence[pos-1].split()[0]+':'+word+':'+tag])
        if pos > 1:
            features.extend(['2PREVBIGRAM:'+sentence[pos-2].split()[0]+':'+sentence[pos-1].split()[0]+':'+tag])
        if pos < len(sentence)-1:
            features.extend(['NEXTBIGRAM:'+word+':'+sentence[pos+1].split()[0]+':'+tag])
        if pos < len(sentence)-2:
            features.extend(['2NEXTBIGRAM:'+sentence[pos+1].split()[0]+':'+sentence[pos+2].split()[0]+':'+tag])

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

def get_features(histories, sentence, model, score, feat):
    result = ''
    for history in histories:
        history_list = history.split()
        if len(history_list) > 0 and history_list[2] != 'STOP':
            pos = int(history_list[0]) - 1
            word = sentence[pos].split()[0]
            tag = history_list[2]

            weight = 0
            #bigram = 'BIGRAM:' + history_list[1] + ':' + tag
            t = 'TAG:' + word + ':' + tag
            features = features_set(word, tag, [t], feat, sentence, pos)

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

def train_model(train_file, model_file, feat):
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
                    gold_dict[i] = get_features(gold.split('\n'), sentence.split('\n'), {}, 0, feat)
                histories = call(enum_server, sentence).split('\n')
                scores = get_features(histories, sentence.split('\n'), model, 1, feat)
                tags = call(history_server, scores).split('\n')
                if tags != gold_tags[i]:
                    features = get_features(tags, sentence.split('\n'), {}, 0, feat)
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
    if len(sys.argv) != 4:
        print "python q6.py [train_file] [output_file] [feature_keyword]"
        sys.exit(2)

    train_model(sys.argv[1], sys.argv[2], sys.argv[3])
