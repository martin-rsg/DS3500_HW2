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
import plotly.graph_objects as go

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

    def code_mapping(self, df, src, targ):
        """ map labels in src and targ columns to integers, built in class """

        labels = list(df[src]) + list(df[targ])
        # labels = sorted(list(set(labels)))

        codes = list(range(len(labels)))
        # print(codes)

        lcmap = dict(zip(labels, codes))
        # print(lcmap)

        df['src'] = lcmap
        df['targ'] = lcmap
        print(df)

        return df, labels

    def wordcount_sankey(self, years, word_list=None, k=5):
        """ Sankey diagram
        # Map each text to words using a Sankey diagram, where the thickness of the line
        # is the number of times that word occurs in the text. Users can specify a particular
        # set of words, or the words can be the union of the k most common words across
        # each text file (excluding stop words)."""

        # df = pd.DataFrame.from_dict(self.data['wordcount'])

        df = pd.DataFrame(self.data['wordcount'])
        df = df.fillna(0)
        df.reset_index(inplace=True)
        df["word"] = df["index"].values

        df = df[['word'] + [col for col in df.columns if col != 'word']]
        df = df.drop(['index'], axis=1)

        # Assemble df that fits sankey required input format
        # this is hacky, we know, but in the interest of time this was the best option.
        call, words, occurances = list(), list(), list()
        for i, row in df.iterrows():
            word = row[0]
            for wc_i in range(1, len(row)):
                words.append(word)
                year_idx = wc_i - 1
                doc_name = 'F_' + str(years[year_idx])
                call.append(doc_name)
                occurances.append(row[wc_i])

        sankey_dict = {'file': call,
                       'word': words,
                       'count_word': occurances}

        sankey_df = pd.DataFrame(data=sankey_dict)

        print(sankey_df)

        # Adopted from HW1:

        src = df['filename']
        targ = df['word']
        vals = "count"

        if word_list is not None:
            clean_pd = pd.DataFrame()
            # change targ to df['word'] where word is in the word list
            for word in word_list:
                df_to_add = df.loc[df['word'] == word]
                clean_df = pd.concat[clean_df, df_to_add]
                df = clean_df
        else:
            df_top_words = df.groupby(by='word').sum()
            print("df top words", df_top_words)
            top_words = df_top_words.head(k)
            print("top words", top_words)

            for word in top_words:
                df_to_add = df.loc[df['word'] == word]
                clean_df = pd.concat[clean_df, df_to_add]
                df = clean_df

        df, labels = self.code_mapping(df, src, targ)

        if vals:
            value = df[vals]
        else:
            value = [1] * df.shape[0]

        link = {'source': df[src], 'target': df[targ], 'value': value}

        node = {'pad': 100, 'thickness': 10,
                'line': {'color': 'black', 'width': 10},
                'label': labels}

        sk = go.Sankey(link=link, node=node)
        fig = go.Figure(sk)
        fig.show()

def compare_num_words(self):
        """This is an example, we probably shouldnt include this"""
        num_words = self.data['numwords']
        for label, nw in num_words.items():
            plt.bar(label, nw)
        plt.show()

def load_stop_words(line_list):
    """ A list of common or stop words. These get filtered from each file automatically """
    stop_list = []
    for line in line_list:
        split_list = line.split()
        length = len(split_list)
        last_word = split_list[length - 1]
        if line != '':
            stop_list.append(last_word)
    return(stop_list)
