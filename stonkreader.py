"""
filename: textastic.py

description: A reusable library for text analysis and comparison
"""

from collections import Counter, defaultdict
import random as rnd
import pandas as pd
import matplotlib.pyplot as plt


class Stonkreader:

    def __init__(self):
        """Constructor"""
        self.data = defaultdict(dict)
        self.prices = pd.DataFrame()

    def _save_results(self, label, results):
        for k, v in results.items():
            self.data[k][label] = v

    @staticmethod
    def _default_parser(filename):

        ''' we need to make our own here'''

        results = {
            'wordcount': Counter("to be or not to be".split(" ")),
            'numwords': rnd.randrange(10, 50)
        }
        return results

    def load_text(self, filename, label=None, parser=None):
        if parser is None:
            results = Stonkreader._default_parser(filename)
        else:
            results = parser(filename)

        if label is None:
            label = filename

        self._save_results(label, results)

    def load_prices(self, filename):
        """ Load daily prices in """
        self.prices = pd.read_csv(filename)
        self.prices.set_axis(['Date', 'Close_Price'], axis=1, inplace=True)
        self.prices.set_index('Date', inplace=True)

    def run_sentiment_analysis(self):
        pass

    def _load_sentences(self):
        """ splits up sentences, adds new feild for self.data """
        ' run a sentance parser'

    def make_sankey(self):
        """ Sankey diagram """

    def compare_num_words(self):
        """This is an example, we probably shouldnt include this"""
        num_words = self.data['numwords']
        for label, nw in num_words.items():
            plt.bar(label, nw)
        plt.show()
