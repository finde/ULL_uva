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
    d = 10.

    # create column
    for (doc, cats) in categories:
        # for cat in cats:
        # if cat not in df.columns:
        # df[cat] = ""
        # v = every word that appear more than 10 times in the corups,
        # w = top 300 frequent words and

        #open the doc
        with open('brown/' + doc) as cfile:
            for lines in cfile:
                if lines == '\n':
                    continue

                sentences = lines.split(' ')

                for index, tagged_word in enumerate(sentences):
                    end = index + int(d / 2)
                    start = int(np.max([0, index - d / 2]))

                    window = sentences[start:end]
                    for w_idx, w in enumerate(sentences[start:end]):
                        if not w in df.columns:
                            df.ix[tagged_word.strip(), w.strip()] = 1
                        else:
                            df.ix[tagged_word.strip(), w.strip()] += 1

                    print window, start, end


    # add word

    print df['mystery']