import sys
import time
from heapq import *
import AST
import numpy as np

from parser import Parser

def depthH(node, target):
    return abs(node.depth() - target.depth())

targetOpDict = None

def numOpsH(node, target):
    global targetOpDict

    if targetOpDict == None:
        targetOpDict = target.numOps()

    nodeOpDict = node.numOps()

    commonKeys = set(targetOpDict.keys()) | set(nodeOpDict.keys())

    total = 0
    for key in commonKeys:
        keyCount = 0
        if key in nodeOpDict:
            keyCount = nodeOpDict[key]

        if key in targetOpDict:
            keyCount = abs(targetOpDict[key] - keyCount)

        total += keyCount
    return total

def countConsts(node):
    if isinstance(node, AST.Const):
        return 1

    if isinstance(node, AST.BinaryOp):
        return countConsts(node.getFirstChild()) + countConsts(node.getSecondChild())

    return countConsts(node.getChild())

def constH(node, target):
    return abs(countConsts(target) - countConsts(node))

def search(start, target, heur):
    heap = []
    score = heur(start, target)
    heappush(heap, (score, [start, None]))
    found = False
    visited = {}
    last = None

    startDepth = start.depth()
    targetDepth = target.depth()
    maxDepth = max(startDepth, targetDepth) + np.sqrt(startDepth + targetDepth)

    while (not found) and len(heap)>0:
        node = heappop(heap)
        node = node[1]
        allNeigh = node[0].getNeighbors()
        neigh = list(filter(lambda x: x.depth() < maxDepth, allNeigh))
        for n in neigh:
            if n==target:
                found = True
                last = [target, node]
                break
            elif str(n) not in visited:
                visited[str(n)] = True
                nn = n.getNeighbors()
                if len(nn)==0:
                    score = heur(n, target)
                else:
                    n2 = np.random.choice(nn)
                    score = heur(n2, target)
                #score = heur(n, target)
                item = (score, [n, node])
                heappush(heap, item)
    if last==None:
        print('The expressions are not logically equivalent.')
        return found
    else:
        print('Path found! The expressions are logically equivalent!')
        printPath(last)
        return found

def printPath(node):
    if node[1]==None:
        print(node[0])
    else:
        printPath(node[1])
        print(node[0])

def main():
    if len(sys.argv) != 4:
        raise Exception('Invalid number of arguments')

    argKeys = {"depth": depthH, "numOps": numOpsH, "constCount": constH}
    p = Parser()
    start = p.parse(sys.argv[1])
    target = p.parse(sys.argv[2])
    h = argKeys[sys.argv[3]]
    s = time.time()
    res = search(start, target, h)
    e = time.time()
    print("Tree Depth Heuristic Elapsed Time: %s" % (e-s))

if __name__ == '__main__':
    main()
