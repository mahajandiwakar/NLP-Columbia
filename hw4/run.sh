#!/bin/bash
echo '_______________________________________\n'
echo 'QUESTION 4\n'
echo '_______________________________________\n'
echo 'Running the program'
now=$(date +"%T")
echo "Current time : $now"
python q4.py tag.model tag_dev.dat tag_dev.out
now=$(date +"%T")
echo "Current time : $now"
echo 'Evaluating performance'
python eval_tagger.py tag_dev.key tag_dev.out


echo '_______________________________________\n'
echo 'QUESTION 5\n'
echo '_______________________________________\n'
echo 'Running the program'
now=$(date +"%T")
echo "Current time : $now"
python q5.py tag_train.dat suffix.model
echo 'Suffix model generated: suffix.model\n'
echo 'Using q4 again to tag\n'
python q4.py suffix.model tag_dev.dat tag_dev_q5.out
now=$(date +"%T")
echo "Current time : $now"
echo 'Evaluating performance'
python eval_tagger.py tag_dev.key tag_dev_q5.out

echo '_______________________________________\n'
echo 'QUESTION 6\n'
echo '_______________________________________\n'
echo 'Running the program, Trainig using various features\n'
now=$(date +"%T")
echo "Current time : $now"
python q6.py tag_train.dat prefix.model prefix
python q6.py tag_train.dat presuf.model suff
python q6.py tag_train.dat word.model word
python q6.py tag_train.dat wordBi.model wordsBigrams
python q6.py tag_train.dat wbo.model wbo
echo 'Tagging\n'
python q4.py prefix.model tag_dev.dat tag_dev_pre.out
python q4.py presuf.model tag_dev.dat tag_dev_ps.out
python q4.py word.model   tag_dev.dat tag_dev_word.out
python q4.py wordBi.model  tag_dev.dat tag_dev_wordBi.out
python q4.py wbo.model  tag_dev.dat tag_dev_wbo.out
now=$(date +"%T")
echo "Current time : $now"
echo 'Evaluating results\n'
python eval_tagger.py tag_dev.key tag_dev_pre.out
python eval_tagger.py tag_dev.key tag_dev_ps.out
python eval_tagger.py tag_dev.key tag_dev_word.out
python eval_tagger.py tag_dev.key tag_dev_wordBi.out
python eval_tagger.py tag_dev.key tag_dev_wbo.out
