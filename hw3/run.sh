#!/bin/bash

echo '_______________________________________\n'
echo 'QUESTION 4: IBM Model 1\n'
echo '_______________________________________\n'
echo 'Running the program'
echo 'Extacting corpus.en.gz & corpus.de.gz'
python IBM_Model1.py corpus.en.gz corpus.de.gz > aligment_model1.txt
echo 'Top words for dev can be found at: devwords_Top10.txt\n'
echo 'Alignment results can be found at: aligment_model1.txt\n'
echo 't values have been saved as: tvalModel1.pkl\n'


echo '_______________________________________\n'
echo 'QUESTION 5: IBM Model 2\n'
echo '_______________________________________\n'
echo 'Running the program, using tvals from IBM Model 1'
echo 'Extacting corpus.en.gz & corpus.de.gz'
python IBM_Model2.py corpus.en.gz corpus.de.gz tvalModel1 > aligment_model2.txt
echo 'Alignment results can be found at: aligment_model2.txt\n'
echo 'q values have been saved as: qvalModel.pkl\n'


echo '_______________________________________\n'
echo 'QUESTION 6: Unscrambled\n'
echo '_______________________________________\n'
echo 'Running the program, using tvals qvals from IBM Model 1 & 2'
python UnScramble.py tvalModel1 qvalModel original.de scrambled.en
echo 'Unscrambled results can be found at: unscrambled.en\n'
echo 'Evaluating results\n'
python eval_scramble.py unscrambled.en original.en