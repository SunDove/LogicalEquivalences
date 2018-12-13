import sys
import time
from heapq import *
import AST
import numpy as np
import json
from math import inf

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

def countParents(tup):
    if tup[1]==None:
        return 1
    return 1 + countParents(tup[1])

def search(start, target, heur, pr=True, limit=20):
    heap = []
    score = heur(start, target)
    heappush(heap, (score, [start, None]))
    found = False
    visited = {}
    last = None

    if start == target:
        found = True
        last = [target, None]

    startDepth = start.depth()
    targetDepth = target.depth()
    maxDepth = max(startDepth, targetDepth) + np.sqrt(startDepth + targetDepth)

    while (not found) and len(heap)>0:
        node = heappop(heap)
        node = node[1]
        c = countParents(node)
        if c>=limit:
            continue
        allNeigh = node[0].getNeighbors()
        neigh = list(filter(lambda x: x.depth() < maxDepth, allNeigh))
        for n in allNeigh:
            if n==target:
                found = True
                last = [target, node]
                break
            elif str(n) not in visited:
                visited[str(n)] = True
                '''
                if len(nn)==0:
                    score = heur(n, target)
                else:
                    n2 = np.random.choice(nn)
                    score = heur(n2, target)
                '''
                score = heur(n, target)
                item = (score, [n, node])
                heappush(heap, item)
    if last==None:
        print('The expressions are not logically equivalent.')
        return found
    else:
        print('Path found! The expressions are logically equivalent!')
        if pr:
            AST.printPath(last)
        return found

def main():
    maxDepth = inf
    if len(sys.argv) == 5:
        maxDepth = int(sys.argv[4])
    elif len(sys.argv) != 4:
       raise Exception('Invalid number of arguments')

    argKeys = {"depth": depthH, "numOps": numOpsH, "constCount": constH}
    h = argKeys[sys.argv[1]]
    results = {}
    p = Parser()
    start = p.parse(sys.argv[2])
    target = p.parse(sys.argv[3])

    s = time.time()
    res = search(start, target, h, pr=True, limit=maxDepth)
    e = time.time()
    print(res)

if __name__ == '__main__':
    main()
