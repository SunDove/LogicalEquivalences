# Logical Equivalences

An automated proof solver for propositional logical equivalences.

## Language Grammar
Our parser supports booleans, single character variables, Ands, Ors, Nots, Conditionals, and Biconditionals.

| Atom          | Symbol         |
| -             | -              |
| Boolean       | 'T' or 'F'     |
| Variable      | 'a', 'b', etc. |
| And           | '^'            |
| Or            | 'v'            |
| Not           | '~'            |
| Conditional   | '->'           |
| BiConditional | '[=]'          |

All operations must be enclosed in their own set of parentheses. For example, `avbvc` is invalid, and must be written as `(avb)vc` or `av(bvc)`.

## Usage
There are four main executables that can be used to solve logical equivalences: `BFS.py`, `Heur1.py`, `Heuristic.py`, and `MLHeuristic.py`.

### `BFS.py`
This solves logical equivalences using a breadth first algorithm.

It can be run from the command line by typing:
```bash
$ python3 BFS.py 'start' 'end'
```
where `start` is the first logical expression and `end` is the second logical expression.
After executing this, `BFS.py` should tell you if the inputs are logically equivalent and output a set of steps from start to end if they are.

### `Heur1.py`
This is a deprecated file that solves logical equivalences using the depth comparison heuristic.

To run it, enter:
```bash
$ python3 Heur1.py 'start' 'end'
```

from a terminal where `start` is the first logical expression and `end` is the second logical expression.
After executing this, `Heur1.py` should tell you if the inputs are logically equivalent and output a set of steps from start to end if they are.

### `Heuristic.py`
This file can be used to run all heuristic algorithms including the depth comparison heuristic from `Heur1.py`.

To run it, enter
```bash
$ python3 Heuristic.py heuristic 'start' 'end' maxDepth
```

Where `heuristic` is the type of heuristic you would like to use, `start` and `end` are logical expressions, and maxDepth is an optional integer maximum depth for the search.

The possible values for `heuristic` are detailed below:
| argument   | heuristic |
| -          | -         |
| depth      | AST depth comparison |
| numOps     | Number of operations comparison |
| constCount | Comparison of the number of variables and booleans in the expression (inefficient)|

### `MLHeuristic.py`
This file can be used to run a weighted heuristic combination or find weights for a weighted heuristic combination.

To find a weighted heuristic combination, enter
```bash
$ python3 MLHeuristic.py
```
at a terminal. The program will output a list of durations for each search it runs using genetically selected weights. This will take a while. After running it's training searches, `MLHeuristic.py` will output a list of efficient weights that can be used in future searches.

Note: sometimes, the program will print 'search did not terminate in time'. This is normal and happens when a poorly weighted search does not terminate after 10 seconds.

To run a weighted heuristic combination, enter
```bash
$ python3 MLHeuristic.py 'start' 'end' depthWeight numOpsWeight numConstsWeight
```

From a terminal where `start` and `end` are logical expressions, and `depthWeight`, `numOpsWeight`, and `numConstWeight` are decimal values for the depth, number of operations, and number of constants heuristics respectively.
