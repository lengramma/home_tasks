from sys import argv
import PrsParser
import XmlParser

def main(argv):
    '''Usage
    python prsxmlparser.py input output
    '''
    if len(argv) == 3:
        if '.xml' in argv[2]:
            XmlParser.start(argv[2], argv[1])
        if '.prs' in argv[2]:
            PrsParser.start(argv[1], argv[2])
    else:
        print(main.__doc__)

if __name__=='__main__':
    main(argv)