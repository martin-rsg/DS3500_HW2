import json
import re
from collections import Counter


def json_parser(filename):
    """ Unused in this analysis because our data was txt """

    f = open(filename)
    raw = json.load(f)
    text = raw['text']
    words = text.split(" ")
    wc = Counter(words)
    num = len(words)
    return {'wordcount': wc, 'numwords': num}


def txt_parser_CIQ(filename, sr):
    """ Loads in txt data copied in from S&P Capital IQ Transcripts, and cleans punctuation and newlines """
    with open(filename) as f:
        lines = [line.strip() for line in f]

    words_nested = [line.split(" ") for line in lines]
    words = [word for sublist in words_nested for word in sublist if word != '']
    # remove periods, capitalization
    end_punct = [",", ".", "!", "?", ":", ";"]
    clean_words = list()
    for word in words:
        l_word = word.lower()
        if l_word in sr.stop_words:
            continue
        if l_word[-1] in end_punct:
            clean_words.append(l_word[:-1])
    wc = Counter(clean_words)
    num = len(clean_words)
    return {'wordcount': wc, 'numwords': num}


def split_into_sentences(filename):
    """ Taken from stackexchange with a few modifications,
    https://stackoverflow.com/questions/4576077/how-can-i-split-a-text-into-sentences

    Sentiment analysis requires sentence inputs. Because of periods located within sentences "Mr. ",
    simply splitting on periods wouldn't work. This function catches the vast majority of edge cases, and can
    accurately split the entirety of Huckleberry Finn into sentences.

    I made minor modifications to account for frequent new line occurances.

    This function feeds into txt_sentence_parser"""

    with open(filename) as f:
        text = str(f.readlines())

    alphabets = "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"

    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "”" in text: text = text.replace(".”", "”.")
    if "\"" in text: text = text.replace(".\"", "\".")
    if "!" in text: text = text.replace("!\"", "\"!")
    if "?" in text: text = text.replace("?\"", "\"?")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip().replace("\\n", "").replace("'', ", "") for s in sentences]

    return sentences


def txt_sentence_parser(filename, sr=None):
    """ splits text into sentences, returned as dict """
    sentences = split_into_sentences(filename)
    return {'sentences': sentences}
