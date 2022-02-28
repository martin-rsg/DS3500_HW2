from matplotlib import pyplot as plt
from wordcloud import WordCloud

import stonkreader_parsers as sp
from stonkreader import Stonkreader


def main():
    sr = Stonkreader()
    sr.load_stop_words('stopwords.txt')
    sr.load_text('Annual_Earnings_Calls/2016_Annual_Call.txt', 'F_2016', parser=sp.txt_parser_CIQ)
    sr.load_text('Annual_Earnings_Calls/2017_Annual_Call.txt', 'F_2017', parser=sp.txt_parser_CIQ)
    sr.load_text('Annual_Earnings_Calls/2018_Annual_Call.txt', 'F_2018', parser=sp.txt_parser_CIQ)
    sr.load_text('Annual_Earnings_Calls/2019_Annual_Call.txt', 'F_2019', parser=sp.txt_parser_CIQ)
    sr.load_text('Annual_Earnings_Calls/2020_Annual_Call.txt', 'F_2020', parser=sp.txt_parser_CIQ)

    sr.load_text('Annual_Earnings_Calls/2016_Annual_Call.txt', 'F_2016', parser=sp.txt_sentence_parser)
    sr.load_text('Annual_Earnings_Calls/2017_Annual_Call.txt', 'F_2017', parser=sp.txt_sentence_parser)
    sr.load_text('Annual_Earnings_Calls/2018_Annual_Call.txt', 'F_2018', parser=sp.txt_sentence_parser)
    sr.load_text('Annual_Earnings_Calls/2019_Annual_Call.txt', 'F_2019', parser=sp.txt_sentence_parser)
    sr.load_text('Annual_Earnings_Calls/2020_Annual_Call.txt', 'F_2020', parser=sp.txt_sentence_parser)

    sr.load_prices('F_Daily_Close_Prices.csv')
    # print(sr.prices)

    years = [2016, 2017, 2018, 2019, 2020]
    sr.wordcount_sankey(years)

    file_list=['Annual_Earnings_Calls/2016_Annual_Call.txt', 'Annual_Earnings_Calls/2017_Annual_Call.txt', 'Annual_Earnings_Calls/2018_Annual_Call.txt',
    'Annual_Earnings_Calls/2019_Annual_Call.txt', 'Annual_Earnings_Calls/2020_Annual_Call.txt']

    text = open('Annual_Earnings_Calls/2016_Annual_Call.txt').read()
    wordcloud = WordCloud().generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

    text1 = open('Annual_Earnings_Calls/2017_Annual_Call.txt').read()
    wordcloud1 = WordCloud().generate(text1)
    plt.imshow(wordcloud1)
    plt.axis("off")
    plt.show()


    text2 = open('Annual_Earnings_Calls/2018_Annual_Call.txt').read()
    wordcloud2 = WordCloud().generate(text2)
    plt.imshow(wordcloud2)
    plt.axis("off")
    plt.show()

    text3 = open('Annual_Earnings_Calls/2019_Annual_Call.txt').read()
    wordcloud3 = WordCloud().generate(text3)
    plt.imshow(wordcloud3)
    plt.axis("off")
    plt.show()

    text4 = open('Annual_Earnings_Calls/2020_Annual_Call.txt').read()
    wordcloud4 = WordCloud().generate(text4)
    plt.imshow(wordcloud4)
    plt.axis("off")
    plt.show()







    # pp.pprint(sr.data)
    # sr.compare_num_words()


if __name__ == '__main__':
    main()
