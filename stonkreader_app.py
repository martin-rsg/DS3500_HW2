
from stonkreader import Stonkreader
import stonkreader_parsers as sp
import pprint as pp

def main():
    sr = Stonkreader()
    # sr.load_text('AAPL_Q1.txt', 'A')
    # sr.load_text('SLB_Q4.txt', 'B')
    ''' this is broken, do not use '''
    sr.load_text('Annual_Earnings_Calls/Ford Motor Company, Q4 2021 Earnings Call, Feb 08, 2022.rtf',
                 'F_2022',
                  parser=sp.rtf_parser_CIQ)
    pp.pprint(sr.data)
    # sr.compare_num_words()


if __name__ == '__main__':
    main()