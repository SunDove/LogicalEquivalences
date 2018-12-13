import sys
import time
import json

from parser import Parser
from AST import printPath

def BFS(start, target, pr=True):
    queue = [(start, None)]
    found = False
    last = None
    ind = 0
    visited = {}
    if start == target:
        last = (target, None)
        found = True
    while (not found) and len(queue[ind:])>0:
        node = queue[ind]
        ind+=1
        neighbors = node[0].getNeighbors()
        for n in neighbors:
            if n==target:
                found = True
                last = (target, node)
                break
            elif str(n) not in visited:
                visited[str(n)] = True
                queue.append((n, node))
    if last==None:
        print('The expressions are not logically equivalent.')
        return False
    else:
        print('Path found! The expressions are logically equivalent!')
        if pr:
            printPath(last)
        return True

def main():
    if len(sys.argv) != 3:
        raise Exception('Invalid number of arguments')

    p = Parser()

    start = p.parse(sys.argv[1])
    target = p.parse(sys.argv[2])
    s = time.time()
    res = BFS(start, target)
    e = time.time()

if __name__ == '__main__':
    main()
