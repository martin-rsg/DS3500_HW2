"""
filename: textastic.py

description: A reusable library for text analysis and comparison
"""

from collections import Counter, defaultdict
import random as rnd
import pandas as pd
import matplotlib.pyplot as plt
import pprint as pp
from textblob import TextBlob
import statistics
import datetime as dt

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

    def run_sentiment_analysis(self, sentiment_type='polarity'):
        """ Runs a textblob sentiment analysis and adds the results to self.data """

        sentences = self.data['sentences']

        # Loop through sentences in {self.data}[sentences]
        for k, v in sentences.items():
            if sentiment_type == 'polarity':
                sentiment_score = statistics.mean([tuple(TextBlob(sentence).sentiment)[0] for sentence in v])

            elif sentiment_type == 'subjectivity':
                sentiment_score = statistics.mean([tuple(TextBlob(sentence).sentiment)[1] for sentence in v])

            else:
                print(f'NO SUCH SENTIMENT TYPE "{sentiment_type}"')

            # Add the results to self.data
            results = {'sentiment': sentiment_score}
            self._save_results(k, results)

        print('SENTIMENT SCORES')
        pp.pprint(self.data['sentiment'])

    def compare_sentiment_stockprice(self, years):
        """ Years is the range of years to plot (can't be more than number of labels)

            This compares the average sentiment of the Q4 annual call (occurs in February) to the stock performance
            for the following year.

            A more robust analysis might look at returns instead of prices, but the point of this function
            is to establish a framework that can easily be modified to make data more granular, or to use
            stock returns instead of absolute prices"""

        close_prices = list()
        # get year-end stock price closes
        counter = 0
        for i, row in self.prices.iterrows():
            cur_date = dt.datetime.strptime(i, "%b-%d-%Y")
            if counter > 0 and cur_date.year > prev_date.year and cur_date.year in years:
                close_prices.append(close_price)
            close_price = row['Close_Price']
            prev_date = cur_date
            counter += 1

        # extract sentiments
        sentiments = []
        for k, v in self.data['sentiment'].items():
            sentiments.append(v)

        x = sentiments
        y = close_prices

        plt.plot(x, y, "o")
        for i in range(len(x)):
            plt.text(x[i], y[i], years[i])
        plt.xlabel("annual earnings call sentiment")
        plt.ylabel("following year ending stock price")
        plt.show()

    def make_sankey(self):
        """ Sankey diagram """

    def compare_num_words(self):
        """This is an example, we probably shouldnt include this"""
        num_words = self.data['numwords']
        for label, nw in num_words.items():
            plt.bar(label, nw)
        plt.show()
