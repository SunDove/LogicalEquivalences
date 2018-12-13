import sys
import time
from heapq import *
import AST
import numpy as np
import json

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
            printPath(last)
        return found

def printPath(node):
    if node[1]==None:
        print(node[0])
    else:
        printPath(node[1])
        print(node[0])

def main():
    #if len(sys.argv) != 4:
    #    raise Exception('Invalid number of arguments')

    argKeys = {"depth": depthH, "numOps": numOpsH, "constCount": constH}
    results = {}
    p = Parser()
    start = p.parse('(pv(pv(pvT)))')
    target = p.parse('T')
    h = (lambda x, y: 1)


    for i in range(5, 26):
        print(i)
        for j in range(10):
            s = time.time()
            res = search(start, target, (lambda x, y: 1), pr=False, limit=i)
            e = time.time()
            if i in results:
                results[i].append(e-s)
            else:
                results[i] = [e-s]
    with open('depthlimit.json', 'w') as out:
        out.write(json.dumps(results))

    '''
    s = time.time()
    res = search(start, target, h, True, 30)
    e = time.time()
    print("Tree Depth Heuristic Elapsed Time: %s" % (e-s))



    cases = [
        ('(avb)vc', 'av(bvc)'),
        ('~(p->q)', 'p^~q'),
        ('~(pv(~p^q))', '~p^~q'),
        ('(p^q)->(pvq)', 'T'),
        #('(pvq)^((~pvr)->(pvq))', 'T')
    ]

    p = Parser()
    parsed = [(p.parse(c[0]), p.parse(c[1])) for c in cases]
    print(parsed)
    sums = []

    for i in range(8):
        sum = 0
        for c in parsed:
            start = c[0]
            target = c[1]
            s = time.time()
            res = search(start, target, depthH, False, 28)
            e = time.time()
            sum+=e-s
        sums.append(sum)
    with open('DEP_res.json', 'w') as file:
        file.write(json.dumps(sums))
    '''

if __name__ == '__main__':
    main()
