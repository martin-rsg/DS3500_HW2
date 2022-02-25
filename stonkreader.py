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
import wordcloud as wc


class Stonkreader:

    def __init__(self):
        """Constructor"""
        self.data = defaultdict(dict)
        self.prices = pd.DataFrame()
        self.stop_words = []

    def _save_results(self, label, results):
        for k, v in results.items():
            self.data[k][label] = v

    @staticmethod
    def _default_parser():
        results = {
            'wordcount': Counter("to be or not to be".split(" ")),
            'numwords': rnd.randrange(10, 50)
        }
        return results

    def load_text(self, filename, label=None, parser=None):
        if parser is None:
            results = Stonkreader._default_parser()
        else:
            results = parser(filename, self)

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

        print(df[src])

        labels = list(df[src]) + list(df[targ])
        # labels = sorted(list(set(labels)))

        print('labels')
        print(labels)

        codes = list(range(len(labels)))

        print('codes')
        print(codes)

        lcmap = dict(zip(labels, codes))
        df = df.replace({src: lcmap, targ: lcmap})
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

        # init clean_df for storing new df with top words
        clean_df = pd.DataFrame()
        if word_list is not None:
            # change targ to df['word'] where word is in the word list
            for word in word_list:
                df_to_add = df.loc[df['word'] == word]
                clean_df = clean_df.append(df_to_add)

        else:
            clean_df = df.copy(deep=True)
            clean_df['sum_words'] = clean_df.sum(axis=1)
            clean_df = clean_df.sort_values(by=['sum_words'], ascending=False)
            clean_df = clean_df.head(k)
            clean_df.drop('sum_words', inplace=True, axis=1)

        df = clean_df

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

        src = 'word'
        targ = 'file'
        vals = "count_word"

        sankey_df, labels = self.code_mapping(sankey_df, src, targ)

        if vals:
            value = sankey_df[vals]
        else:
            value = [1] * sankey_df.shape[0]

        link = {'source': sankey_df[src], 'target': sankey_df[targ], 'value': value}

        node = {'pad': 100, 'thickness': 10,
                'line': {'color': 'black', 'width': 10},
                'label': labels}

        sk = go.Sankey(link=link, node=node)
        fig = go.Figure(sk)
        fig.show()

    def word_cloud(self, file_list):
        rows = 2
        columns = 3
        fig = plt.figure(figsize=(columns, rows), dpi=200)
        plt.title(f'A {rows}X{columns} Array of Presidential Poetry Readings')
        plt.axis('off')

        cloud = wc.WordCloud()
        img = cloud.generate(file_list)
        fig.add_subplot(rows, columns)
        plt.imshow(img)

        # Remove inner axis labels
        for ax in fig.get_axes():
            ax.label_outer()

        # Save figure to disk
        plt.savefig('image_array.png')
        plt.show()

    def compare_num_words(self):
        """This is an example, we probably shouldnt include this"""
        num_words = self.data['numwords']
        for label, nw in num_words.items():
            plt.bar(label, nw)
        plt.show()

    def load_stop_words(self, file):
        """ A list of common or stop words. These get filtered from each file automatically """

        stop_list = []
        with open(file) as f:
            for line in f:
                split_list = line.split()
                length = len(split_list)
                last_word = split_list[length - 1]
                if line != '':
                    stop_list.append(last_word.lower())
        return stop_list
