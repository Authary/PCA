POLYADIC CONCEPT ANALYSIS
====

This module provides functions for computing formal concepts and rules bases in both bidimensional and multidimensional formal contexts. It makes extensive use of Takeaki Uno's software for computing minimal transversals of hypergraphs (http://research.nii.ac.jp/~uno/dualization.html).

Functionalities:<br/>
-Context -> Concepts<br/>
-Context -> Canonical implication basis<br/>
-Context -> Proper premises implication basis<br/>
-Context -> Association rules basis<br/>
-Context -> Introducer concepts<br/>
-Concepts -> Covering relation of the set of concepts partially ordered by the inclusion relation on their last n-1 components<br/>
-Set x Implications -> Minimal generators of Set under logical closure by the implications

It is based on, among other papers,<br/>
-*On Implication Bases in n-Lattices*. Alexandre Bazin. Discrete Applied Mathematics 2020.<br/>
-*A Depth-first Search Algorithm for Computing Pseudo-closed Sets*. Alexandre Bazin. Discrete Applied Mathematics 2018.<br/>
-*Représentation condensée de règles d’association multidimensionnelles*. Alexandre Bazin, Aurélie Bertaux, Christophe Nicolle. EGC 2019.<br/>
-*Reduction and Introducers in d-contexts*. Alexandre Bazin and Giacomo Kahn. ICFCA 2019.<br/>
-*k-Partite Graphs as Contexts*. Alexandre Bazin and Aurélie Bertaux. CLA 2018.


LEGAL STUFF
====

You are free to use this module.<br/>
If you do something interesting with it, please tell Alexandre Bazin: contact [at] alexandrebazin [dot] com.


STRUCTURES
===============

*FORMAL CONTEXTS*

Formal contexts take the form of tuples (C,s_1,...,s_n) in which s_1,...,s_n are the sizes of the n dimensions (integers) and C is the incidence relation, i.e. a list of n-elements lists. The elements of dimensions are integers.
Example:


| |	0|	1|	2|	3|	4|
|---| ---| ------|--------|------|------| 
|0|	x|	x|	|	|	|
|1|	|	x|	x|	x|	|
|2|	|	x|	|	x|	x|
|3|	|	|	x|	|	x|
|4|	|	|	|	x|	x|

is represented as ([[0,0],[0,1],[1,1],[1,2],[1,3],[2,1],[2,3],[2,4],[3,2],[3,4],[4,3],[4,4]],5,5).


*CONCEPTS*

Formal concepts are lists containing n sets.
Example:
The formal concept (12,13) is represented by [{1, 2}, {1, 3}].


*IMPLICATIONS*

Implications are lists containing two sets, the premise and the conclusion.
Example:
The implication 12 -> 123, valid in the previous context, is represented by [set([12]),set([123])].


*ASSOCIATION RULES*

Association rules are lists containing two sets, the premise and the conclusion, and a float, the confidence.
Example:
The association rule 1 -> 13, with confidence 2/3 in the previous context, is represented by [{1}, {1, 3}, 0.6666666666666666].


*MAPPING TABLE*

A dictionary mapping lists to integers.
Example:
{0: [0, 0],
 1: [0, 1],
 2: [0, 2],
 3: [1, 0],
 4: [1, 1],
 5: [1, 2],
 6: [2, 0],
 7: [2, 1],
 8: [2, 2]} means that [0, 0] is mapped to 0, [0, 1] to 1...


Useful Functions
================

*concepts(context)*<br/>
INPUT: a formal context<br/>
OUTPUT: a list containing all the formal concepts of the context


*properPremises(context)*<br/>
INPUT: a formal context<br/>
OUTPUT: a list containing the implications of the proper premises basis AND a dictionary mapping lists to integers. for multidimensional contexts<br/>
WARNING : If the context contains more than 2 dimensions, it is transformed into a bidimensional context by replacing the n-1 last dimensions by their cartesian product. Use the dictionary to retrieve the elements of the cartesian product.


*NextClosureDG(context)*<br/>
INPUT: a formal context<br/>
OUTPUT: a list containing the implications of the canonical (Duquenne-Guigues) basis AND a dictionary mapping lists to integers for multidimensional contexts<br/>
WARNING : If the context contains more than 2 dimensions, it is transformed into a bidimensional context by replacing the n-1 last dimensions by their cartesian product. Use the dictionary to retrieve the elements of the cartesian product. Uses the Next Closure algorithm.


*associationRules(context)*<br/>
INPUT: a formal context<br/>
OUTPUT: a list of association rules


*buildNeighbouringRelation(concepts)*<br/>
INPUT: a list of concepts<br/>
OUTPUT: a list of 2-elements lists representing the covering relation of the set of concepts partially ordered by the inclusion relation on their last n-1 components<br/>
WARNING: Naive algorithm, can take some time.


*logicalClosure(Set,Rules)*<br/>
INPUT: a set (Set) and a list of implications (Rules)<br/>
OUTPUT: the logical closure of Set by Rules


*allMinGensImp(Set,Implis)*<br/>
INPUT: a set (Set) closed under logical closure by a list of implications (Implis)<br/>
OUTPUT: a list containing the minimal generators of Set under Implis


*minTrans(hypergraph)*<br/>
INPUT: a hypergraph in the form of a list of integer lists (edges)<br/>
OUTPUT: the minimal transversals of the hypergraph<br/>
WARNING: Calls shd.exe.


*introducersDimension(context,dimension)*<br/>
INPUT: a formal context and a dimension ({0,...n})<br/>
OUTPUT: the list of concepts that introduce an element of the dimension


*allIntroducers(context)*<br/>
INPUT: a formal context<br/>
OUTPUT: the list of all introducer concepts of the context


HOW TO USE
================

context = ([[0,0,0],[0,0,1],[0,1,0],[1,0,0],[2,2,2]],3,3,3)

```python
#Compute the formal concepts
concepts  =  concepts(context)
print(concepts)
[[{0, 1, 2}, {0, 1, 2}, set()],
 [{0, 1}, {0}, {0}],
 [{0}, {0, 1}, {0}],
 [{0}, {0}, {0, 1}],
 [{0, 1, 2}, set(), {0, 1, 2}],
 [set(), {0, 1, 2}, {0, 1, 2}],
 [{2}, {2}, {2}]]

#Compute the Duquenne-Guigues basis
Implis, table = NextClosureDG(context)
print(Implis)
[[{7}, {0, 1, 2, 3, 4, 5, 6, 7, 8}],
 [{6}, {0, 1, 2, 3, 4, 5, 6, 7, 8}],
 [{5}, {0, 1, 2, 3, 4, 5, 6, 7, 8}],
 [{4}, {0, 1, 2, 3, 4, 5, 6, 7, 8}],
 [{3}, {0, 1, 3}],
 [{2}, {0, 1, 2, 3, 4, 5, 6, 7, 8}],
 [{1}, {0, 1, 3}],
 [{0, 8}, {0, 1, 2, 3, 4, 5, 6, 7, 8}]]
print(table)
{0: [0, 0],
 1: [0, 1],
 2: [0, 2],
 3: [1, 0],
 4: [1, 1],
 5: [1, 2],
 6: [2, 0],
 7: [2, 1],
 8: [2, 2]}

#Print the fifth implication with the tuples
print([table[x] for x in Implis[4][0]]," -> ",[table[x] for x in Implis[4][1]])
[[1, 0]]  ->  [[0, 0], [0, 1], [1, 0]]
```
