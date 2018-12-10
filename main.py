import sys
from parser import Parser
from AST import *

def main():
    p = Parser()
    e = p.parse(sys.argv[1])
    print(e, [str(n) for n in e.getNeighbors()])

if __name__ == '__main__':
    main()
