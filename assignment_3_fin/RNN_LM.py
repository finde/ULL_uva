import numpy
import time


class Mikolov_RNNLM:
    def __init__(self, voc_size, N=10):
        self.N = N  # number of neurons in hidden layer
        self.vocabulary_size = voc_size  # size of vocabulary (number of word types)

        # initialization of parameters
        self.U = numpy.random.randn(N, voc_size)  # weights from one-hot repr to hidden layer
        self.W = numpy.random.randn(N, N)  # weights from previous time to hidden layer

        self.V = numpy.random.randn(voc_size, N)  # weights from hidden layer to the output layer (softmax layer)

    def train(self, batches, learning_rate=.9, time_lag=1):
        idx = numpy.arange(len(batches))
        numpy.random.shuffle(idx)
        for n, i in enumerate(idx):
            if (n + 1) % int(len(batches) / 5) == 0:
                print n + 1, 'of', len(idx)
            batch = batches[i]
            s_hist = [numpy.zeros(self.N)]
            w_hist = [0]
            for w in batch:
                s = 1 / (numpy.exp(- numpy.dot(self.W, s_hist[-1]) - self.U[:, w_hist[-1]]) + 1)
                z = numpy.dot(self.V, s)
                y = numpy.exp(z)
                y = y / y.sum()

                y[w] -= 1
                err = [numpy.dot(y, self.V) * s * (s - 1)]
                for t in xrange(min(time_lag, len(s_hist) - 1)):
                    st = s_hist[-1 - t]
                    err.append(numpy.dot(err[-1], self.W) * st * (1 - st))

                # backpropagate
                w_hist.append(w)
                s_hist.append(s)
                self.V -= numpy.outer(y, s * learning_rate)
                for t in xrange(len(err)):
                    self.U[:, w_hist[-1 - t]] += err[t] * learning_rate

    def fit(self, X):
        return self._softmax(numpy.dot(self.U, X))

    @staticmethod
    def _softmax(X):
        e = numpy.exp(X)
        dist = e / numpy.sum(e)
        return dist
