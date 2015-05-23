#!/bin/sh

echo '_______________________________________\n'
echo 'QUESTION 4 & 5\n'
echo '_______________________________________\n'
echo 'Replacing rare words.'
python RareReplacer.py parse_train.dat parse_train_rare.dat
echo 'Replaced dataset: parse_train_rare.dat\n'
echo 'Generating counts'
python count_cfg_freq.py parse_train_rare.dat > cfg_rare.counts
echo 'Generated counts: cfg_rare.counts\n'
echo 'Running CKY algo'
python CKY.py cfg_rare.counts parse_train_rare.dat > results45
echo 'Evaluation'
python eval_parser.py parse_dev.key results45


echo '_______________________________________\n'
echo 'QUESTION 6\n'
echo '_______________________________________\n'
echo 'Replacing rare words.'
python RareReplacer.py parse_train_vert.dat parse_train_vert_rare.dat
echo 'Replaced dataset: parse_train_rare.dat\n'
echo 'Generating counts'
python count_cfg_freq.py parse_train_vert_rare.dat > cfg_rare_vert.counts
echo 'Generated counts: cfg_rare.counts\n'
echo 'Running CKY algo'
python CKY.py cfg_rare_vert.counts parse_train_vert_rare.dat > results6
echo 'Evaluation'
python eval_parser.py parse_dev.key results6
