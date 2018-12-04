import sys

from parser import Parser

def BFS(start, target):
    print(start, target)
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
        printPath(last)
        return True

def printPath(node):
    if node[1]==None:
        print(node[0])
    else:
        printPath(node[1])
        print(node[0])

def main():
    if len(sys.argv) != 3:
        raise Exception('Invalid number of arguments')
    p = Parser()
    start = p.parse(sys.argv[1])
    target = p.parse(sys.argv[2])
    return BFS(start, target)

if __name__ == '__main__':
    main()
