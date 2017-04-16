# Data Structures and Algorithm Efficiency

This repository contains a set of problems whose solutions involves choosing a clever data sctructure and algorithm, in order to improve the scalability of the problem, i.e. to achieve the best possible runtime order $O$. The solutions to all the questions are found in the python file `solutions.py`, which also contains a few basic tests to make sure the functions work as intended.

## Questions

The following questions were answered as part of the Udacity Machine Learning Engineer Nanodegree.

### Question 1

Given two strings `s` and `t`, determine whether some anagram of `t` is a substring of `s`. For example: if `s = "udacity"` and `t = "ad"`, then the function returns `True`. Your function definition should look like: `question1(s, t)` and return a boolean `True` or `False`.

#### Chosen answer

While it's possible to consider all permutations of `t` and see if any one of them is in `s`, this approach is inefficient: it will take *O*(*m*! *n*) where *m* = len(*t*) and *n* = len(*s*) . My approach is to break up the strings into lists of characters (`t_list` and `s_list`). We then only go through `s_list` once: if we get to a character in `t`, we remove this character from `t_list`. If after a number of such steps `t_list` has length zero, some order of the letter in `t` was contained in `s` and we can return `True`. If we get to a character in `s` that is not contained in `t`, we reset `t_list` to its original value and effectively start over deleting letters from it. This will have the approximate efficiency *O*(*n*). It is much more targeted to the correct permutation of letters in t than the brute force approach, and going through a single list (`s_list`) is very fast.

### Question 2

Given a string `a`, find the longest palindromic substring contained in `a`. Your function definition should look like `question2(a)`, and return a string.

#### Chosen answer

A first approach could be to reverse the string so it reads backwards, list all substrings, and see which of these substrings is the longest one which appears in the original string. The time for this would be *O*(*n*<sup>3</sup>), because making all substrings would be *O*(*n*<sup>2</sup>) and for each one we need to perform a search *O*(*n*). The approach I took searches for all palindromic centers, by going through the string only once, and when the previous and the next characters are the same (or we have a double), declare this to be the center of a palindrome. For each center, I then find out how long the palindromic substring is (by growing it in both directions from the center), and simply keep the longest. This algorithm has runtime *O*(*n*), because of the search to find the centers and because the time it takes to find the length of each palindrome does not grow with n. My approach treats the string much like a list, rather than a stack or a tree. It is possible that turning the string into a binary search tree, our palindromic search to find centers could be reduced to *O*(log(*n*)).

### Question 3

Given an undirected graph *G*, find the minimum spanning tree within *G*. A minimum spanning tree connects all vertices in a graph with the smallest possible total weight of edges. Your function should take in and return an adjacency list structured like this:
```
{'A': [('B', 2)],
 'B': [('A', 2), ('C', 5)], 
 'C': [('B', 5)]}
 ```
Vertices are represented as unique strings. The function definition should be `question3(G)`.

#### Chosen answer

This problem seems similar to the shortest-length problem: from a given vertex, we could look for the shortest path is to all the other vertices. However, it may be that this choice of connectivity it globally sub-optimal, i.e. that it is only optimal with regards to that particular vertex. For example, consider four nodes that are fully connected to each other, laid out in the arrangement of a square with two diagonals. The edges along the outer square have weight 1 and the diagonals have weight 1.5. The minimum spanning tree has weight 3, achieved by taking three of the outer edges of the square. From a given vertex, the shortest length to all other vertices involves using the diagonal, giving a spanning tree of length 3.5. The solution I chose makes use of sets and is similar to hierarchical clustering. We begin with each node belonging to a separate "cluster", where the clusters are in the form of sets. We then go through the list of edges, ordered by weight. The smallest-weight edge which connects two nodes belonging to different sets is chosen as the next edge in the algorithm. We then merge the two sets. We proceed in this way until all sets have been merged. The list of the chosen edges specifies a minimum spanning tree. This algorithm has efficiency *O*(*E*) where *E* is the number of edges in the graph.

### Question 4

Find the least common ancestor between two nodes on a binary search tree. The least common ancestor is the farthest node from the root that is an ancestor of both nodes. For example, the root is a common ancestor of all nodes on the tree, but if both nodes are descendents of the root's left child, then that left child might be the lowest common ancestor. You can assume that both nodes are in the tree, and the tree itself adheres to all BST properties. The function definition should look like `question4(T, r, n1, n2)`, where `T` is the tree represented as a matrix, where the index of the list is equal to the integer stored in that node and a 1 represents a child node, `r` is a non-negative integer representing the root, and `n1` and `n2` are non-negative integers representing the two nodes in no particular order. For example, one test case might be

```
question4([[0, 1, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [1, 0, 0, 0, 1],
           [0, 0, 0, 0, 0]],
          3,
          1,
          4)
```
and the answer would be 3.

#### Chosen answer

In a binary search tree, since all descendants on either side of a node are smaller or larger than that node, we are easily able to determine what the least common ancestor of any two nodes is: it is the ancestor node whose value lies between the two chosen nodes. If the two chosen nodes are in a descendant relationship to each other, e.g. one is the child of the other, then the least common ancestor is the node preceding the parent node. To solve this problem we only need to flow down the binary search tree, and stop when we find a node that lies between the two chosen nodes or is a parent to one of the two nodes. Since flowing down BSTs has efficiency *O*(log(*n*)) (for decently balanced trees -- otherwise it is *O*(*n*) in the worse case where the BST is equal to a linked list), we expect our algorithm to have this same efficiency.

### Question 5

Find the element in a singly linked list that's m elements from the end. For example, if a linked list has 5 elements, the 3rd element from the end is the 3rd element. The function definition should look like `question5(ll, m)`, where `ll` is the first node of a linked list and `m` is the "mth number from the end". You should copy/paste the Node class below to use as a representation of a node in the linked list. Return the value of the node at that position.

```
class Node(object):
  def __init__(self, data):
    self.data = data
    self.next = None
```