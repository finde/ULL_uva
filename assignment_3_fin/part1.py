import subprocess

__author__ = 'finde'

import pandas as pd
import pickle
import numpy as np

if __name__ == '__main__':
    """
        In this model first you have to form a word-context matrix M.
        Rows of this matrix are your vocabulary (v) and the columns are context words (w).

        The value for cell (r, c) of the matrix is the number of times that the cth context word
        have appeared as the context of the rth word, given the context with windows
        size of d.

        Parameter d adjusts the number of words in the neighbourhood of
        your target word that should considered as context. For example for d = 10,
        you have to consider 5 words after and before a word as its context.

        1. Calculate matrix M for the Brown corpus with these parameters:
            v = every word that appear more than 10 times in the corups,
            w = top 300 frequent words and
            d = 10.

        2. Run Singular Value Decomposition on M and approximate it using top 30 and 60 singular values.
            Look at the entries of approximated matrices compare them against vectors of the full matrix.
            What do you see?
            Are they sparse or dense?

        3. Evaluate the induced vectors for all three matrices on similarity and relatedness task, and report them.

        4. Once you are sure that your code is working, run the whole pipeline on Wikipedia dump
            (if you are not sure how to clean the dump, email the T.A.) and
            report your scores for similarity and relatedness tasks.
            For Wikipedia, limit your vocabulary v to top 2000 words.

        5. Analyze your results! for what types of words do you see a good performance (correct prediction)?
            Where do your vectors perform poorly?
            How is it related to the frequency of the words.
            Which one of the tasks is harder, similarity or relatedness?
    """

    with open('brown/categories.pickle') as corpus:
        categories = pickle.load(corpus)

    df = pd.DataFrame()
    d = 10

    temp_file = 'brown_cleaned'
    subprocess.check_output(['./clean_brown.sh', str('brown/c???'), temp_file, str(d / 2)])
    frequent_words = subprocess.check_output(['./get_freq_words.sh', temp_file, str(d)]).split('\n')
    n_lines = subprocess.check_output(['wc -l', temp_file])

    # v = every word that appear more than 10 times in the corups,
    # w = top 300 frequent words and

    # open the doc
    # get clean lines
    with open('brown_cleaned') as file:

        for n, lines in enumerate(file):

            sentences = lines.split(' ')
            if len(sentences) < d / 2:
                continue

            for index, tagged_word in enumerate(sentences):
                end = int(np.min([len(sentences), index + int(d / 2) + 1]))
                start = int(np.max([0, index - int(d / 2) - 1]))

                if not tagged_word in frequent_words:
                    continue

                # append at the last
                window = sentences[start:index - 1] + sentences[index + 1:end]

                for w_idx, word in enumerate(window):
                    if not word in df.columns:
                        df.ix[tagged_word, word] = 1
                    elif not tagged_word in df.index:
                        df.ix[tagged_word, :] = 0
                        df.ix[tagged_word, word] += 1
                    else:
                        df.ix[tagged_word, word] += 1

        if n % 1000 == 0:
            print "%s/%s [%s%%]" % (n, n_lines, n / n_lines)

    # store df to csv
    df.fillna(0)
    df.to_csv('data/brown_all_no_punctuation.csv')

    # add word

    print df['mystery']