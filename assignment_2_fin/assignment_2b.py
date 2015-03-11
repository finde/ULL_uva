from __future__ import division

__author__ = 'finde'

from scipy.stats import rv_discrete
import sys
import json
import os.path
from random import uniform, choice
from assignment_2a import represents_int, reject_outlier, plot_hist
import numpy as np
from matplotlib import pyplot

SAMPLE = 50000


def is_marked(probability=None):
    if not probability:
        probability = [0.6, 0.4]
    return ['', '*'][rv_discrete(values=([0, 1], probability)).rvs()]


def parse_numeric(num, markers=None):
    """
    should generate this rule
    S -> NZ S
    S -> D
    :param num: integer input
    :param markers: if will be re-random when markers is empty
    :return: tree, marked_tree, stored_markers, number
    """
    num = list(reversed(list(str(num))))

    tree = ''
    marked_tree = []
    pruned_tree = ''
    stored_markers = []
    if len(num) == 1:
        tree = '(S (D "%s"))' % (num[0])
    else:
        for idx, i in enumerate(num):
            if markers is None:
                _is_mark = is_marked()
                _is_mark_2 = is_marked()
            else:
                [_is_mark, _is_mark_2] = markers[idx]

            stored_markers.append([_is_mark, _is_mark_2])

            # mark randomly
            if idx == 0:
                tree = '(D%s "%s")' % (_is_mark, i)
                pruned_tree = tree

                if _is_mark == '*':
                    marked_tree.append('(D "%s")' % i)
                    pruned_tree = '_D'

            elif idx == len(num) - 1:  # TOP
                tree = '(S (NZ%s "%s") %s)' % (_is_mark, i, tree)

                if _is_mark == '*':
                    marked_tree.append('(NZ "%s")' % i)
                    marked_tree.append('(S _NZ %s)' % pruned_tree)
                else:
                    marked_tree.append('(S (NZ "%s") %s)' % (i, pruned_tree))

            else:
                tree = '(S%s (NZ%s "%s") %s)' % (_is_mark, _is_mark_2, i, tree)
                cur_pruned_tree = '(S%s (NZ%s "%s") %s)' % (_is_mark, _is_mark_2, i, pruned_tree)

                if _is_mark_2 == '*':
                    marked_tree.append('(NZ "%s")' % i)
                    cur_pruned_tree = '(S%s _NZ %s)' % (_is_mark, pruned_tree)

                if _is_mark == '*':
                    if _is_mark_2 == '*':
                        marked_tree.append('(S NZ %s)' % pruned_tree)
                    else:
                        marked_tree.append('(S (NZ "%s") %s)' % (i, pruned_tree))
                    cur_pruned_tree = '_S'

                pruned_tree = cur_pruned_tree

    return tree, marked_tree, stored_markers


def tsg2num(string):
    return int(''.join(
        [s.replace('"', '').replace(')', '').replace('(', '') for s in string.split(' ') if s.startswith('"')]))


class ElementaryTrees:
    def __init__(self):
        self.tree_table = {}
        self.root_table = {}
        self.derivation_banks = []

        self._temp_tree_table = {}
        self._temp_root_table = {}
        self._derivation_banks = []

    def insert(self, _derivation_bank):
        (_, e_trees, _) = _derivation_bank

        self.derivation_banks.append(_derivation_bank)

        for st in e_trees:

            if st in self.tree_table:
                self.tree_table[st] += 1
            else:
                self.tree_table.update({st: 1})

            root = self.get_root(st)
            if root in self.root_table:
                self.root_table[root] += 1
            else:
                self.root_table.update({root: 1})

    def remove(self, __derivation_bank):
        (_, e_trees, _) = __derivation_bank

        for st in e_trees:
            if st in self.tree_table:
                self.tree_table[st] -= 1
                self.root_table[self.get_root(st)] -= 1

    @staticmethod
    def get_root(tree):
        return tree.split(' ')[0].replace('(', '')

    def count_tree(self, tree):
        if tree in self.tree_table:
            return self.tree_table[tree]
        else:
            return 0

    def count_root(self, tree):
        root = self.get_root(tree)
        return self.root_table[root]

    def preserve_the_state(self):
        self._temp_tree_table = self.tree_table
        self._temp_root_table = self.root_table
        self._derivation_banks = self.derivation_banks
        pass

    def revert_to_pristine(self):
        self.tree_table = self._temp_tree_table
        self.root_table = self._temp_root_table
        self.derivation_banks = self._derivation_banks
        pass

    def get_likelihood(self, derivations_tree):
        likelihood = 1

        for d_tree in derivations_tree:
            likelihood *= self.count_tree(d_tree) * 1.0 / self.count_root(d_tree)

        return likelihood

    def to_json(self, filename):
        with open(filename, 'w') as outfile:
            json.dump({"tree_table": self.tree_table,
                       "root_table": self.root_table,
                       "derivation_banks": self.derivation_banks}, outfile)
        pass

    def from_json(self, filename):
        with open(filename, 'r') as json_data:
            data = json.load(json_data)

        self.tree_table = data['tree_table']
        self.root_table = data['root_table']
        self.derivation_banks = data['derivation_banks']
        pass


class MetropolisHastings:
    def __init__(self, elementary_table, method='addRule'):
        """

        :param method: addRule or removeRule
        :return:
        """
        self.method = method
        self.elementary_table = elementary_table
        self.candidates = []
        self.likelihood_history = []

    def generate_candidate(self, candidate=None, marker=None):
        """
        if candidate empty, it will be picked from cache
        if marker empty, it will reshuffle the marker
        :param candidate:
        :param marker:
        :return:
        """

        if candidate is None:
            candidate = choice(self.elementary_table.derivation_banks)

        (tsg, _, _) = candidate

        return parse_numeric(tsg2num(tsg), marker)

    @staticmethod
    def change_marker(marker, method='addRule'):

        m_length = len(marker)
        # pick index
        if m_length == 0:
            return marker

        flat = np.array(marker).reshape((1, 2 * m_length))

        if method == 'addRule':
            available = [_index for _index, f in enumerate(flat[0]) if
                         f == '' and _index is not 0 and _index is not len(flat[0]) - 1]

            if len(available) == 0:
                return marker

            flat[0][choice(available)] = '*'

        else:
            available = [_index for _index, f in enumerate(flat[0]) if
                         f == '*' and _index is not 0 and _index is not len(flat[0]) - 1]
            if len(available) == 0:
                return marker

            flat[0][choice(available)] = ''

        return flat.reshape(m_length, 2)

    def compute_likelihood(self, candidate, new_candidate):

        self.elementary_table.preserve_the_state()

        # compute MLE of the old candidate
        (_, tree, _) = candidate
        likelihood_old = self.elementary_table.get_likelihood(tree)

        # remove the trees from the old_derivations_tree
        self.elementary_table.remove(candidate)
        self.elementary_table.insert(new_candidate)

        # compute MLE of the new candidate
        (_, tree, _) = new_candidate
        likelihood_new = self.elementary_table.get_likelihood(tree)

        self.elementary_table.revert_to_pristine()

        return likelihood_old, likelihood_new

    def train(self, iteration=10):

        accepted = 0
        for it in xrange(iteration):

            # create random candidate
            candidate = self.generate_candidate()

            # apply changes
            (_, _, marker) = candidate
            new_marker = self.change_marker(marker, self.method)
            new_candidate = self.generate_candidate(candidate, new_marker)

            likelihood_old, likelihood_new = self.compute_likelihood(candidate, new_candidate)

            if likelihood_new > likelihood_old:
                # TODO: think about the burn-in
                accepted += 1.0
                self.elementary_table.insert(new_candidate)
                self.likelihood_history.append(np.max([likelihood_old, likelihood_new]))

            else:
                u = uniform(0.0, 1.0)
                if u < (likelihood_new / likelihood_old):
                    # TODO: think about the burn-in
                    accepted += 1.0
                    self.elementary_table.insert(new_candidate)
                    self.likelihood_history.append(np.max([likelihood_old, likelihood_new]))

            if it % 1000 == 0:
                print '(%s, %s)' % (it, iteration)

        # burn = int(np.ceil(burn_in * len(self.candidates)))
        # self.candidates = self.candidates[burn:len(self.candidates)]
        return accepted / iteration

    def generate_sample(self, n_sample):
        e = self.elementary_table
        # pick S rule
        sample = []
        rules = {'S': [x for x, val in e.tree_table.iteritems() if x.startswith('(S')],
                 'NZ': [x for x, val in e.tree_table.iteritems() if x.startswith('(NZ')],
                 'D': [x for x, val in e.tree_table.iteritems() if x.startswith('(D')]}

        proba = {
            'S': [val * 1.0 / e.root_table['S'] for x, val in e.tree_table.iteritems() if x.startswith('(S')],
            'NZ': [val * 1.0 / e.root_table['NZ'] for x, val in e.tree_table.iteritems() if x.startswith('(NZ')],
            'D': [val * 1.0 / e.root_table['D'] for x, val in e.tree_table.iteritems() if x.startswith('(D')]}

        for iSam in xrange(n_sample):
            string = rules['S'][rv_discrete(values=(np.arange(len(rules['S'])), proba['S'])).rvs()]

            while string.find('_') > 0:
                string = string.replace('_S', rules['S']
                [rv_discrete(values=(np.arange(len(rules['S'])), proba['S'])).rvs()], 1)
                string = string.replace('_NZ', rules['NZ']
                [rv_discrete(values=(np.arange(len(rules['NZ'])), proba['NZ'])).rvs()], 1)
                string = string.replace('_D', rules['D']
                [rv_discrete(values=(np.arange(len(rules['D'])), proba['D'])).rvs()], 1)

            sample.append(tsg2num(string))

            if iSam % 1000 == 0:
                print '(%s, %s)' % (iSam, n_sample)

        return sample


if __name__ == '__main__':

    e_tables = ElementaryTrees()

    cache_file = 'cache.json'
    if not os.path.isfile(cache_file):
        if len(sys.argv) >= 2:
            numbers_data_file = sys.argv[1]
        else:
            numbers_data_file = '../data/wsj01-21-without-tags-traces-punctuation-m40.txt_numbers'

        numbers = []
        with open(numbers_data_file) as f:
            for line in f:
                if represents_int(line):
                    numbers.append(int(line))

        numbers = reject_outlier(numbers)

        trees = []
        for n in numbers:
            e_tables.insert(parse_numeric(n))

        e_tables.to_json(cache_file)
    else:
        e_tables.from_json(cache_file)

    mHas = MetropolisHastings(elementary_table=e_tables, method='addRule')
    print mHas.train(iteration=200)
    plot_hist(mHas.generate_sample(10), 'mhasting_add_sample.png')

    pyplot.plot(mHas.likelihood_history)
    pyplot.ylim([0, 1.2])
    pyplot.savefig('mhasting_add_likelihood.png')
    pyplot.clf()


    # mHas = MetropolisHastings(elementary_table=e_tables, method='removeRule')
    # print mHas.train(200000, 0.5, numbers)
    # plot_hist(mHas.candidates, 'mhasting_remove.png')


