
from stonkreader import Stonkreader
import stonkreader_parsers as sp
import pprint as pp

def main():
    sr = Stonkreader()
    sr.load_text('file1.txt', 'A')
    sr.load_text('file2.txt', 'B')
    sr.load_text('myfile.json', 'J', parser=sp.json_parser)
    pp.pprint(sr.data)
    sr.compare_num_words()


if __name__ == '__main__':
    main()