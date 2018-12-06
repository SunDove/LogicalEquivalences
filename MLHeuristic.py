import sys
import time
from heapq import *
import AST
import numpy as np
import multiprocessing as m

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

def heur(s, t, h, w):
    v = np.array([hi(s, t) for hi in h])
    return np.matrix.dot(v, w)

def search(start, target, heurs, weights, pr=True):
    heap = []
    score = heur(start, target, heurs, weights)
    heappush(heap, (score, [start, None]))
    found = False
    visited = {}
    last = None

    startDepth = start.depth()
    targetDepth = target.depth()
    maxDepth = max(startDepth, targetDepth) + (startDepth + targetDepth)/2

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
                score = heur(n, target, heurs, weights)
                item = (score, [n, node])
                heappush(heap, item)
    if last==None:
        if pr:
            print('The expressions are not logically equivalent.')
        return found
    else:
        if pr:
            print('Path found! The expressions are logically equivalent!')
            printPath(last)
        return found

def printPath(node):
    if node[1]==None:
        print(node[0])
    else:
        printPath(node[1])
        print(node[0])

def newPop(population, scores):
    choose = []
    for i in range(10):
        choose.append(heappop(scores)[1].array)
    pop = [c for c in choose]
    for i in range(80):
        old = np.random.choice(range(len(choose)))
        old = choose[old]
        mute = np.multiply(np.random.choice([-1, 1], size=3), 0.1)
        pop.append(np.add(old, mute))
    for i in range(10):
        pop.append(np.random.rand(1, 3)[0])
    print(len(pop))
    return pop

class StupidArray:

    def __init__(self, a):
        self.array = a

    def __lt__(self, other):
        return 0

    def __str__(self):
        return str(self.array)

    def __repr__(self):
        return str(self.array)

def main():
    # sys.setrecursionlimit(1000)
    if len(sys.argv) != 3:
        raise Exception('Invalid number of arguments')

    p = Parser()
    start = p.parse(sys.argv[1])
    target = p.parse(sys.argv[2])
    population = np.random.rand(100, 3) #3 is number of heuristics
    best = []
    searchTimeout = 10 # In seconds
    for i in range(100):
        best = []
        print(best)
        for p in population:
            searchProcess = m.Process(target=search, args=(start, target, [depthH, numOpsH, constH], p, False))
            s = time.time()
            searchProcess.start()
            searchProcess.join(searchTimeout)
            # res = search(start, target, [depthH, numOpsH, constH], p, False)
            e = time.time()
            if searchProcess.is_alive():
                searchProcess.terminate()
                print("search did not terminate in time")
            else:
                heappush(best, (e-s, StupidArray(p)))
        population = newPop(population, best)
        print(best[0])
        print("%s done" % i)
    s = time.time()
    res = search(start, target, [depthH, numOpsH, constH], best[0].array)
    e = time.time()
    print("Best time: %" % (e-s))
    print("Weights: %s" % best[0])
    #[ 0.90416266  0.60873807 -0.97709181]


if __name__ == '__main__':
    main()
