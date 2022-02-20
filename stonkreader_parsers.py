import json
import textract as tt
from collections import Counter


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
    f = open(filename, 'r')
    text = f.read()
    f.close()
    words = text.split(" ")
    wc = Counter(words)
    num = len(words)
    return {'wordcount': wc, 'numwords': num}


def rtf_parser_CIQ(filename):
    """ BROKEN Loads in msft word data downloaded from S&P Capital IQ Transcripts """
    text = tt.process(filename)
    print(text)
    words = text.split(" ")
    wc = Counter(words)
    num = len(words)
    # return {'wordcount': wc, 'numwords': num}