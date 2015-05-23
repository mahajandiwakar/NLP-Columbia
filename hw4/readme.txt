Natural Language processing

Homework 4

run the script using the following command:

sh ./run.sh

Question 4
---------------

As it can be observed by running the script file that the program got an accuracy of approx 90.5% with
2226/2459 correct tagings.


Question 5
--------------
The accuracy now increased to approx > 92% which can easily be attributed to the inclusion of suffic features.
We noe have 2265/2459 correct taggings.


Question 6
----------------
For this I have experimented with 3 sets of features & their accuracies are given:

1 - Suffix features
    2226 2459 0.905246034974

2 - prefix & suffix features
    2241 2459 0.911346075641

3 - word features
    2263 2459 0.920292801952

4 - Bigram features
    2162 2459 0.879219194795

5 - Word bigrams and others
    2333 2459 0.948759658398


1. Suffix features:

    In Suffix features we incorporate suffixes of length 4 or less (as compared to three or less) found in the word.
    We donot include bigram features here, even then we are able to correctly tag 2226/2459 which is fairly good accuracy on its own

2. Prefix & Suffix features:

    So apart from including the feature 1 we incorporate prefix features of length 4 or less.
    This further improves the accuracy to 91% and we are able to correctly tag 2241/2459.
    This emphasises the importance of incorporating prefix features.

3.  Word Features:

    Here we only work upon the word features. We includes previous two words (w{i-2}, w{i-1}) and the next two words (w{i+1}, w{i+2})
    We further improve the accuracy to 92% correctly classifying 2263/2459.

    Thus we have clearly identified that including next and previous words improves the accuracy.

4. Bigrams:

    Finally I experimented with bigrams of words, using the following combinations:
        w{i-2}+w{i-1}, w{i-1}+w{i}, w{i}+w{i+1}, w{i+1}+w{i+2}

    The accuracy I got for this features was bad at 88% and it could get only 2162/2459

5. Word bigrams and others:

    I found that using features word, bigrams and prefixes and suffixes we get the best accuracy.
    The accuracy jumped to ~95% and correct tagging of 2333/2459
