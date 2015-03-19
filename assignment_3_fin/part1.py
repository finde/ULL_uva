from __future__ import division
import os
import subprocess
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats.stats import pearsonr
from nltk.corpus import brown, stopwords

__author__ = 'finde'


def lines_in_file(f):
    p = subprocess.Popen(['wc', '-l', f],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    out, err = p.communicate()
    return int(out.lstrip(' ').split(' ')[0])


class Part1:
    def __init__(self, source_file, cache_prefix='', stopwords=None):
        self.M = {"no_svd": [], "svd_30": [], "svd_60": []}
        self.source_file = source_file
        self.cache_prefix = cache_prefix
        self.stopwords = stopwords
        pass

    def create_matrix(self, d=10, number_of_features=300, from_file='brown_cleaned',
                      save_to='data/brown_all_no_punctuation.csv', ):

        frequent_words = subprocess.check_output(['./get_freq_words.sh', from_file, str(d)]).split('\n')

        if os.path.isfile(save_to):
            return pd.DataFrame.from_csv(save_to, sep='\t', encoding='utf-8'), frequent_words

        n_lines = lines_in_file(from_file)
        df = pd.DataFrame(index=frequent_words, columns=frequent_words[:number_of_features],
                          data=np.zeros((len(frequent_words), number_of_features)))
        df.fillna(0)

        print "Reading %s lines of corpus" % n_lines

        with open(from_file) as f:
            for n, lines in enumerate(f):
                sentences = lines.split(' ')

                if self.stopwords is not None:
                    sentences = [w for w in sentences if w not in self.stopwords]

                if len(sentences) < 2:
                    continue

                for index, tagged_word in enumerate(sentences):
                    end = int(np.min([len(sentences), index + int(d / 2) + 1]))
                    start = int(np.max([0, index - int(d / 2) - 1]))

                    if tagged_word not in frequent_words:
                        continue

                    window = sentences[start:max(index, index - 1)] + sentences[index + 1:end]
                    for w_idx, word in enumerate(window):
                        if word not in frequent_words[:300]:
                            continue
                        df.ix[tagged_word, word] += 1

                if n % 25 == 0:
                    print "%s/%s [%.2f%%]" % (n, n_lines, n * 100 / n_lines)

        df.to_csv(save_to, sep='\t', encoding='utf-8')
        return df, frequent_words

    @staticmethod
    def similarity_eval(matrix, gold_standard, name='m', save_file=''):
        gs_words = list(gold_standard['word_1'].append(gold_standard['word_2']).drop_duplicates())
        matrix_words = matrix.index.values
        common_words = list(set(gs_words) & set(matrix_words))

        word1 = []
        word2 = []

        gold_standard[name] = 0
        gold_standard['d_' + name] = 0
        for index, r in gold_standard.iterrows():
            if r.word_1 in common_words and r.word_2 in common_words:
                _score = cosine_similarity(matrix.loc[r.word_1], matrix.loc[r.word_2])[0][0] * 10
                gold_standard.ix[index, name] = _score
                gold_standard.ix[index, 'd_' + name] = abs(r.gold - _score)

                # if _diff < 0.3:
                word1.append(r.gold)
                word2.append(_score)

        gold_standard = gold_standard[gold_standard[name] != 0]

        plt.clf()
        plt.xlim(0, 10)
        plt.ylim(0, 10)
        plt.xlabel('gold standard')
        plt.ylabel(name)
        plt.title('Similarity evaluation between gold standard vs %s' % name)
        cm = plt.cm.get_cmap('RdYlBu')
        plt.scatter(word1, word2, alpha=0.5, cmap=cm)
        z = np.polyfit(word1, word2, 1)
        p = np.poly1d(z)
        plt.plot(word1, p(word1), "r-")

        plt.savefig('similarity_eval_' + name)
        return gold_standard

    @staticmethod
    def relatedness_eval(matrix, gold_standard, name='m', save_file=''):
        gs_words = list(gold_standard['word_1'].append(gold_standard['word_2']).drop_duplicates())
        matrix_words = matrix.index.values
        common_words = list(set(gs_words) & set(matrix_words))

        word1 = []
        word2 = []

        gold_standard[name] = 0
        for index, r in gold_standard.iterrows():
            if r.word_1 in common_words and r.word_2 in common_words:
                _score = pearsonr(matrix.loc[r.word_1], matrix.loc[r.word_2])[1] * 10
                gold_standard.ix[index, name] = _score
                gold_standard.ix[index, 'd_' + name] = abs(r.gold - _score)

                # if _diff < 0.3:
                word1.append(r.gold)
                word2.append(_score)

        gold_standard = gold_standard[gold_standard[name] != 0]

        plt.clf()
        plt.xlim(0, 10)
        plt.ylim(0, 10)
        plt.xlabel('gold standard')
        plt.ylabel(name)
        plt.title('Relatedness evaluation between gold standard vs %s' % name)
        cm = plt.cm.get_cmap('RdYlBu')
        plt.scatter(word1, word2, alpha=0.5, cmap=cm)
        z = np.polyfit(word1, word2, 1)
        p = np.poly1d(z)
        plt.plot(word1, p(word1), "r-")

        plt.savefig('relatedness_eval_' + name)
        return gold_standard

    def evaluate(self, matrices, s_gs, r_gs):
        for m in matrices:
            s_gs = self.similarity_eval(matrices[m], s_gs, m)

            print ''
            print '========'
            print ' ', m
            print '========'
            print ''

            print ''
            print '=================='
            print ' ++ Similarity'
            print '=================='
            print ''
            print 'P-value: ', pearsonr(s_gs['gold'], s_gs[m])[1]
            print 'RMSE: ', sqrt(mean_squared_error(s_gs['gold'], s_gs[m]))

            print ''
            print "=== top 10 closest relation [gold & %s] ===" % m
            print s_gs.sort(['d_' + m], ascending=True, axis=0)[list(['word_1', 'word_2', 'd_' + m])].head(10)
            print ''
            print "=== gold top 10 ==="
            print s_gs.sort(['gold'], ascending=False, axis=0)[list(['word_1', 'word_2', 'gold'])].head(10)
            print ''
            print "=== %s top 10 ===" % m
            print s_gs.sort([m], ascending=False, axis=0)[list(['word_1', 'word_2', m])].head(10)

            r_gs = self.relatedness_eval(matrices[m], r_gs, m)

            print ''
            print '=================='
            print ' ++ Relatedness'
            print '=================='
            print ''
            print 'P-value: ', pearsonr(r_gs['gold'], r_gs[m])[1]
            print 'RMSE: ', sqrt(mean_squared_error(r_gs['gold'], r_gs[m]))

            print ''
            print "=== top 10 closest relation [gold & %s] ===" % m
            print r_gs.sort(['d_' + m], ascending=True, axis=0)[list(['word_1', 'word_2', 'd_' + m])].head(10)
            print ''
            print "=== gold top 10 ==="
            print r_gs.sort(['gold'], ascending=False, axis=0)[list(['word_1', 'word_2', 'gold'])].head(10)
            print ''
            print "=== %s top 10 ===" % m
            print r_gs.sort([m], ascending=False, axis=0)[list(['word_1', 'word_2', m])].head(10)

    def single_run(self):
        # 1. calculate Matrix M
        print 'calculating Matrix M'
        M = self.M
        number_of_features = 300
        save_file = self.cache_prefix + 'brown_10_300_no_punctuation'
        M['no_svd'], freq_words = self.create_matrix(10, number_of_features, self.source_file, save_file + '.csv')
        print "..done"


        # 2. Run SVD on 30 and 60
        print 'calculating the SVD'
        if not os.path.isfile(save_file + '_svd_30.csv'):
            U, sigma, V = np.linalg.svd(M['no_svd'])
            V_df = pd.DataFrame(V, columns=M['no_svd'].columns.values)

        n_singular_value = [30, 60]
        for n in n_singular_value:
            print 'approx using %s singular value' % n

            if os.path.isfile(save_file + '_svd_' + str(n) + '.csv'):
                M['svd_' + str(n)] = pd.DataFrame.from_csv(save_file + '_svd_' + str(n) + '.csv', sep='\t',
                                                           encoding='utf-8')
            else:
                approx = np.matrix(U[:, :n]) * np.diag(sigma[:n]) * np.matrix(V[:n, :])
                M['svd_' + str(n)] = pd.DataFrame(approx, index=freq_words, columns=freq_words[:number_of_features])
                M['svd_' + str(n)].to_csv(save_file + '_svd_' + str(n) + '.csv', sep='\t', encoding='utf-8')

            print "Error from actual value: %s" % sqrt(mean_squared_error(M['no_svd'], M['svd_' + str(n)]))
            # the diff should be sparse

        # 3. Evaluation
        sim_gs = pd.DataFrame.from_csv('wordsim353_sim_rel/wordsim_similarity_goldstandard.txt',
                                       sep='\t', index_col=None, header=None)
        sim_gs.columns = ['word_1', 'word_2', 'gold']

        rel_gs = pd.DataFrame.from_csv('wordsim353_sim_rel/wordsim_relatedness_goldstandard.txt',
                                       sep='\t', index_col=None, header=None)
        rel_gs.columns = ['word_1', 'word_2', 'gold']

        self.evaluate(M, sim_gs, rel_gs)


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
    # 1 - 4
    d = 10

    source = 'brown_cleaned'
    if not os.path.isfile(source):
        subprocess.check_output(['./clean_brown.sh', 'brown/c???', source, str(d / 2)])

    # Part1(source, cache_prefix='').single_run()

    # 5. Remove stop words
    source = 'no_sw_brown_cleaned'
    if not os.path.isfile(source):
        subprocess.check_output(['./clean_brown_no_stopwords.sh', 'brown/c???', source])

    Part1(source, cache_prefix='no_sw_', stopwords=stopwords.words('english')).single_run()

    # Part 2
