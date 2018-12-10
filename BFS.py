import sys
import time
import json

from parser import Parser

def BFS(start, target, pr=True):
    queue = [(start, None)]
    found = False
    last = None
    ind = 0
    visited = {}
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

def printPath(node):
    if node[1]==None:
        print(node[0])
    else:
        printPath(node[1])
        print(node[0])

def main():
    #if len(sys.argv) != 3:
    #    raise Exception('Invalid number of arguments')

    cases = [
        ('(avb)vc', 'av(bvc)'),
        ('~(p->q)', 'p^~q'),
        ('~(pv(~p^q))', '~p^~q'),
        ('(p^q)->(pvq)', 'T'),
        #('(pvq)^((~pvr)->(pvq))', 'T')
    ]

    p = Parser()
    parsed = [(p.parse(c[0]), p.parse(c[1])) for c in cases]

    sums = []

    for i in range(8):
        sum = 0
        for c in parsed:
            start = c[0]
            target = c[1]
            s = time.time()
            res = BFS(start, target, False)
            e = time.time()
            sum+=e-s
        sums.append(sum)

    with open('BFS_res.json', 'w') as file:
        file.write(json.dumps(sums))

if __name__ == '__main__':
    main()
