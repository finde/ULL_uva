__author__ = 'finde'

import sys
from matplotlib import pyplot
import random
import itertools
from scipy.stats import rv_discrete
import numpy as np

LIMIT_X = 3500
Y_LIM = 0.1


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def generate_number(prior_dist='uniform', sample=100, prior_proba=None, pitmanYorParam=None):
    '''
    S = root
    D = terminal Natural Numbers
    NZ = terminal Non-Zero Natural Numbers
    ND = Digit Non terminal
    TH = thousands (expanded into two identical items to prevent python issue)
    TH = hundreds (expanded into two identical items to prevent python issue)
    '''

    # problem, to simple grammar rule, does not have flexibility to generate "longer" number
    init_rules = {
        'S': [['D'], ['D', 'S']],
        'D': [['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9'], ['0']]
    }

    rules = {
        'S': [
            ['D'],
            ['NZ', 'D'],
            ['NZ', 'HD'],
            ['NZ', 'TH'],
            ['NZ', 'ND']],  # probability of single digit number vs more-than-one digit number
        'TH': [['D', 'D', 'D'], ['D', 'D', 'D']],
        'HD': [['D', 'D'], ['D', 'D']],  # hundreds
        'ND': [['D'], ['HD'], ['TH'], ['ND', 'ND']],
        'NZ': [['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9']],
        'D': [['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9'], ['0']]
    }

    if not prior_dist == 'uniform' and not prior_dist == 'pitmanYor':
        dist = {
            'S': {},
            'ND': {},
            'TH': {},
            'HD': {},
            'NZ': {},
            'D': {}
        }

        for key in rules.keys():
            dist[key] = rv_discrete(values=(np.arange(len(prior_proba[key])), prior_proba[key]))

    # for pitman-yor, generate the tree, keep track of the frequencies
    if prior_dist == 'pitmanYor':
        # init
        d = pitmanYorParam['d']
        alpha = pitmanYorParam['alpha']

        freq = {
            'S': [0, 0, 0, 0, 0],  # probability of single digit number vs more-than-one digit number
            'TH': [0, 0],
            'HD': [0, 0],  # hundreds
            'ND': [0, 0, 0, 0],
            'NZ': [0, 0, 0, 0, 0, 0, 0, 0, 0],
            'D': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }

    # start
    output = []
    for iSam in xrange(sample):
        string = ['S']

        while True:
            # pick rule
            new_string = [''] * len(string)
            for idx, key in enumerate(string):
                if rules.has_key(key):
                    available_replacement = rules[key]

                    if prior_dist == 'uniform':
                        choice = random.choice(available_replacement)
                    elif prior_dist == 'pitmanYor':
                        # K = number of generated rules (uniq)
                        # d = concentration
                        # alpha = ?
                        # n = number of generated rules


                        K = sum([1 for i in freq[key] if i > 0])
                        n = sum(freq[key])
                        prob_of_choose_new_table = (alpha + d * K) / (n - 1 + alpha)
                        flip_coin = random.random()

                        # new table here can be duplication of the existing table ( so it is equal to the rules )
                        _new_table = available_replacement
                        _occupied_table = [available_replacement[_id] for _id, a in enumerate(freq[key]) if a > 0]

                        if flip_coin < prob_of_choose_new_table:
                            # choose new table
                            if prior_proba is None:
                                proba = [1.0 / len(_new_table)] * len(_new_table)
                            else:
                                proba = prior_proba[key]

                            index = rv_discrete(values=(np.arange(len(_new_table)), proba)).rvs()
                        else:
                            proba = np.zeros(len(_occupied_table))
                            for rule_index, _ in enumerate(_occupied_table):
                                proba[rule_index] = (freq[key][rule_index] - d) * 1.0 / (n - 1 + alpha)

                            index = rv_discrete(values=(np.arange(len(_occupied_table)), proba)).rvs()

                        # update freq
                        if freq[key][index] == 0:
                            K += 1

                        freq[key][index] += 1
                        choice = rules[key][index]

                    else:
                        choice = available_replacement[dist[key].rvs()]

                    # update string
                    new_string[idx] = choice
                else:
                    new_string[idx] = [key]

            string = list(itertools.chain(*new_string))
            if len(string) > 10:
                output.append(100000000)
                break

            if represents_int(''.join(string)):
                output.append(int(''.join(string)))
                break

    return output


def plot_hist(data, filename):
    data = reject_outlier(data)
    bins = np.linspace(-5, LIMIT_X, LIMIT_X + 5)

    pyplot.clf()
    pyplot.hist(data, bins=bins, histtype='step', color='b')
    pyplot.savefig(filename)

    pyplot.clf()
    pyplot.hist(data, bins=bins, histtype='step', normed=True, color='b')
    pyplot.ylim([0, Y_LIM])
    pyplot.xlim([-5, LIMIT_X])
    pyplot.savefig('[NORM]_' + filename)


def reject_outlier(data):
    return [e for e in data if (e < LIMIT_X)]


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        numbers_data_file = sys.argv[1]
    else:
        numbers_data_file = '../data/wsj01-21-without-tags-traces-punctuation-m40.txt_numbers'

    if len(sys.argv) >= 3:
        SAMPLE = int(sys.argv[2])
    else:
        SAMPLE = 10

    numbers = []
    with open(numbers_data_file) as f:
        for line in f:
            if represents_int(line):
                numbers.append(int(line))

    plot_hist(numbers, str(LIMIT_X) + '_' + 'original.png')
    print 'original'

    numbers = generate_number(prior_dist='uniform', sample=SAMPLE)
    plot_hist(numbers, str(LIMIT_X) + '_' + str(SAMPLE) + '_uniform.png')
    print 'uniform'

    # dist 1
    p_dist1 = {
        'S': (0.05, 0.8, 0.05, 0.05, 0.05),  # high probability to create smaller number than 10-99
        'ND': (0.25, 0.25, 0.25, 0.25),
        'TH': (1.0, 0),  # thousands
        'HD': (1.0, 0),  # hundreds
        'NZ': (0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111),  # uniform terminal digit
        'D': (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)  # uniform terminal digit
    }
    numbers = generate_number(prior_dist='dist1', sample=SAMPLE, prior_proba=p_dist1)
    plot_hist(numbers, str(LIMIT_X) + '_' + str(SAMPLE) + '_custom_dist1.png')
    print 'custom distribution 1'

    # dist 2
    p_dist2 = {
        'S': (0.1, 0.05, 0.05, 0.5, 0.3),  # high probability to create thousands
        'ND': (0.25, 0.25, 0.25, 0.25),  # probability of creating bigger number is higher than terminal
        'TH': (1.0, 0),  # thousands
        'HD': (1.0, 0),  # hundreds
        'NZ': (0.1, 0.4, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05),  # non-uniform terminal digit
        'D': (0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.5)  # non-uniform terminal digit
    }
    numbers = generate_number(prior_dist='dist2', sample=SAMPLE, prior_proba=p_dist2)
    plot_hist(numbers, str(LIMIT_X) + '_' + str(SAMPLE) + '_custom_dist2.png')
    print 'custom distribution 2'

    _d = [0.1, 0.3, 0.5, 0.7, 0.9]

    # _alpha should not be 1
    _alpha = [10, 100, 500, 1000, 5000, 10000]

    for __d in _d:
        for __alpha in _alpha:
            numbers = generate_number(prior_dist='pitmanYor', sample=SAMPLE,
                                      pitmanYorParam={'d': __d, 'alpha': __alpha})

            filename = '_'.join([
                'limit_x', str(LIMIT_X),
                'n_sample', str(SAMPLE),
                'd', str(__d),
                'alpha', str(__alpha)
            ]) + '_pitman_yor.png'

            plot_hist(numbers, filename)

            print filename