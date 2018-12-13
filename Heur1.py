import sys
import time
from heapq import *

from parser import Parser
from AST import printPath

def search(start, target):
    heap = []
    score = abs(start.depth()-target.depth())
    heappush(heap, (score, [start, None]))
    found = False
    visited = {}
    last = None
    if start == target:
        found = True
        last = [target, None]
    while (not found) and len(heap)>0:
        node = heappop(heap)
        node = node[1]
        neigh = node[0].getNeighbors()
        for n in neigh:
            if n==target:
                found = True
                last = [target, node]
                break
            elif str(n) not in visited:
                visited[str(n)] = True
                score = abs(n.depth()-target.depth())
                item = (score, [n, node])
                heappush(heap, item)
    if last==None:
        print('The expressions are not logically equivalent.')
        return False
    else:
        print('Path found! The expressions are logically equivalent!')
        printPath(last)
        return True

def main():
    if len(sys.argv) != 3:
        raise Exception('Invalid number of arguments')
    p = Parser()
    start = p.parse(sys.argv[1])
    target = p.parse(sys.argv[2])
    s = time.time()
    res = search(start, target)
    e = time.time()
    print("Tree Depth Heuristic Elapsed Time: %s" % (e-s))

if __name__ == '__main__':
    main()
