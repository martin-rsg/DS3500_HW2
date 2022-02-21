
from stonkreader import Stonkreader
import stonkreader_parsers as sp
import pprint as pp

def main():
    sr = Stonkreader()
    sr.load_text('Annual_Earnings_Calls/2016_Annual_Call.txt', 'F_2016', parser=sp.txt_parser_CIQ)
    sr.load_text('Annual_Earnings_Calls/2017_Annual_Call.txt', 'F_2017', parser=sp.txt_parser_CIQ)
    sr.load_text('Annual_Earnings_Calls/2018_Annual_Call.txt', 'F_2018', parser=sp.txt_parser_CIQ)
    sr.load_text('Annual_Earnings_Calls/2019_Annual_Call.txt', 'F_2019', parser=sp.txt_parser_CIQ)
    sr.load_text('Annual_Earnings_Calls/2020_Annual_Call.txt', 'F_2020', parser=sp.txt_parser_CIQ)

    sr.load_prices('F_Daily_Close_Prices.csv')
    print(sr.prices)


    pp.pprint(sr.data)
    # sr.compare_num_words()


if __name__ == '__main__':
    main()