import json
from collections import Counter
import csv
import pandas as pd
import re

def json_parser(filename):
    f = open(filename)
    raw = json.load(f)
    text = raw['text']
    words = text.split(" ")
    wc = Counter(words)
    num = len(words)
    return {'wordcount': wc, 'numwords': num}


def txt_parser_CIQ(filename):
    """ Loads in txt data copied in from S&P Capital IQ Transcripts """
    with open(filename) as f:
        lines = [line.strip() for line in f]

    words_nested = [line.split(" ") for line in lines]
    words = [word for sublist in words_nested for word in sublist if word != '']
    # remove periods, capitalization
    end_punct = [",",".","!","?",":",";"]
    clean_words = list()
    for word in words:
        print(word)
        l_word = word.lower()
        if l_word[-1] in end_punct:
            clean_words.append(l_word[:-1])
    wc = Counter(clean_words)
    num = len(clean_words)
    return {'wordcount': wc, 'numwords': num}

def txt_sentence_parser(filename):
    """ splits text into sentences, returned as dict """
    f = open(filename, 'r')
    text = f.read()
    f.close()
    words = text.split(" ")




