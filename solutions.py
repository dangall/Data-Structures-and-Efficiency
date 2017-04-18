# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 14:52:31 2017

@author: Daniele
"""

from copy import copy
import numpy as np
from timeit import default_timer as timer

# =============== QUESTION 1 ==================


def turn_to_list(input_string):
    """
    Helper function to question1, which turns a string into a list of
    characters.
    """
    return list(input_string.lower())


def question1(s, t):
    if (s is not None) and (t is not None):
        # We begin by making the lists of letters
        s_list = turn_to_list(s)
        # We will save the t_list to avoid recomputing it multiple times
        original_t_list = turn_to_list(t)
        t_list = copy(original_t_list)
        # We also don't want to recompute len(t) multiple times
        len_t = len(t)

        # Now we go through the characters of s
        for charachter in s_list:
            if charachter in t_list:
                t_list.remove(charachter)
            elif len(t_list) != len_t:
                t_list = copy(original_t_list)
            if len(t_list) == 0:
                return True
    return False

# =============== QUESTION 2 ==================


def length_palindrome(full_string, center, odd=True):
    """
    Helper function that returns the length of the palindrome centered at
    position center in full_string. If the palidrome has even length, set
    odd=False, otherwise set odd=True.
    """
    # We will increase the palindrom simultaneously in both directions from the
    # center. If the two end-points stop being equal to each other, we stop
    # growing the palindrome. We are only given palindromes of a certain minmum
    # length, so we may begin by growing by 2 steps from the center instead of
    # 1.
    steps = 2
    # If we have an even palindrome, we need to shift positions by 1 in order
    # to account for the double-letter at the center of this palindrome.
    if odd:
        shift = 0
    else:
        shift = 1
    # We will look to see whether the letter at position min_pos is equal to
    # that at position max_pos
    min_pos = center - steps + shift
    max_pos = center + steps
    # We grow the palindrome as long as our minimum and maximum don't go out of
    # range for the string
    while ((min_pos >= 0) and
           (max_pos <= len(full_string) - 1) and
           (full_string[min_pos] == full_string[max_pos])):
        steps += 1
        min_pos = center - steps + shift
        max_pos = center + steps
    # Now we know how many steps we have grown our palindrome. The total length
    # is returned
    length = (steps - 1) * 2 + 1 - shift
    return length


def question2(input_string):
    # We begin by making all letters lowercase. We will not remove any
    # characters.

    if input_string is not None and len(input_string) > 0:
        s = input_string.lower()
        longest_palindrome = s[0]
    else:
        return ""

    # First find the centers of the odd-length palindromes
    odd_palindrome_centers = [char_pos for char_pos in range(1, len(s) - 1)
                              if s[char_pos-1] == s[char_pos+1]]
    # Now find the centers of the odd-length palindromes
    even_palindrome_centers = [char_pos for char_pos in range(len(s) - 1)
                               if s[char_pos] == s[char_pos+1]]

    # For each center, we find out how long that palindrome is. If it's longer
    # than longest_palindrome, we replace longest_palindrome by this new
    # palindrome.
    for center in even_palindrome_centers:
        len_palindrome = length_palindrome(s, center, odd=False)
        if len_palindrome > len(longest_palindrome):
            longest_palindrome = s[center - (len_palindrome)/2 + 1:
                                   center + (len_palindrome)/2 + 1]

    for center in odd_palindrome_centers:
        len_palindrome = length_palindrome(s, center, odd=True)
        if len_palindrome > len(longest_palindrome):
            longest_palindrome = s[center - (len_palindrome-1)/2:
                                   center + (len_palindrome-1)/2 + 1]
    return longest_palindrome

# =============== QUESTION 3 ==================


def list_edges(key_node, val_node):
    """
    Takes a node "key_node" and a list of edges it connects to "val_node", and
    returns the list of edges in the format [({key_node, node1}, edge1_weight),
    ...] E.g. key_node = "B", val_node = [("A", 1), ("C", 2)] returns
    [({"A", "B"}, 1), ({"B", "C"}, 2)]
    """
    return [({key_node, node}, weight) for node, weight in val_node]


def add_edge_output_graph(edge_to_add, graph):
    """
    Helper function that takes an edge of the form ({"node1", "node2"},
    node_weight) and adds it to the list of edges in the graph, in the form
    {"node1": [("node2", node_weight)], "node2": [("node1", node_weight)]} .
    """
    for val in edge_to_add[0]:
        graph[val] = graph[val] + [(list(edge_to_add[0].difference({val}))[0],
                                    edge_to_add[1])]
    return graph


def question3(input_graph):
    # Begin by making each node a separate "cluster". all_sets is the list of
    # such clusters
    all_sets = [{key} for key in input_graph.keys()]

    # Make an empty output graph, e.g. {"A": [], "B": [], ...}, which is the
    # spanning tree. We'll fill it in as we build the spanning tree
    output_graph = dict([(key, []) for key, val in input_graph.items()])

    # Make a list of all edges. This list will contain duplicates, since
    # input_graph contains duplicate information for an undirected graph
    # (each undirected edge appears twice).
    edge_list = sum([list_edges(key, val) for key, val in input_graph.items()],
                    [])
    # We now sort the edge list by the edge-weights.
    edge_list = sorted(edge_list, key=lambda x: x[-1])

    # Now we'll go through each edge and, if it merges two separate clusters
    # in all_sets, we add it to output_graph.
    for pos in range(len(edge_list)):
        # nodes_to_join are the nodes joined by the edge at edge_list[pos]
        nodes_to_join = edge_list[pos][0]
        # We check what the intersection is for each cluster in all_sets.
        # indices_to_join tells us at which indices there is a nonzero
        # intersection
        indices_to_join = np.where([len(nodes_to_join.intersection(clust)) > 0
                                    for clust in all_sets])[0]
        # If we have more than 1 index, we are merging two separate clusters.
        if len(indices_to_join) > 1:
            # We add this edge to the output spanning tree
            output_graph = add_edge_output_graph(edge_list[pos], output_graph)
            # Merge the two clusters. In the first position take the union of
            # the two
            all_sets[indices_to_join[0]] = all_sets[indices_to_join[0]].union(
                                           all_sets[indices_to_join[-1]])
            # The other cluster is now redundant as it has been absorbed into
            # the first cluster
            all_sets.pop(indices_to_join[-1])
    return output_graph

# =============== QUESTION 4 ==================


def children_values(input_bst, currentnode):
    """
    Helper function that returns the value of its children
    """
    return np.where(input_bst[currentnode])[0]


def LCA_Q(ancestor, node1, node2):
    """
    Returns True / False depending on whether the value of ancestor lies
    between node1 and node2, which determines whether it is the least common
    ancestor.
    """
    if node1 < ancestor < node2:
        return True
    elif node2 < ancestor < node1:
        return True
    else:
        return False


def question4(input_bst, root_node, node1, node2):
    if (len(np.array(input_bst).shape) == 2 and
        np.array(input_bst).shape[0] == np.array(input_bst).shape[1] and
        np.array(input_bst).shape > max([root_node, node1, node2])):
        # lca_node will be set to the value of the least common ancenstor (LCA)
        lca_node = None
        # Begin with the root node
        current_node = root_node
        # We go down the tree until we found the LCA
        while lca_node is None:
            # If the current node is between node1 and node2, we have found the
            # LCA
            if LCA_Q(current_node, node1, node2):
                lca_node = current_node
            else:
                children = children_values(input_bst, current_node)
                if current_node < node1:
                    # we need to select the larger of the two children and
                    # procced along the tree in that direction
                    next_node = children[-1]
                else:
                    # we need to select the smaller of the two children and
                    # procced along the tree in that direction
                    next_node = children[0]
                if next_node in [node1, node2]:
                    lca_node = current_node
                else:
                    current_node = next_node
        return lca_node
    else:
        print "This input is invalid"
        return None

# =============== QUESTION 5 ==================


class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None


def make_array(first_node):
    # We will go through all elements in the linked list and make an array
    # with each of the consecutive values in the list.
    start_node = first_node
    if start_node is not None:
        array = [start_node.data]
        current_node = start_node
        while current_node.next is not None:
            array.append(current_node.next.data)
            current_node = current_node.next
    else:
        array = []
    return array


def question5(first_node, m):
    if first_node is not None:
        return make_array(first_node)[-m]


def time_question5(first_node):
    """
    Auxiliary function used to time the answer to question 5.
    """
    alltimes = []
    for ii in range(2000):
        start = timer()

        question5(first_node, 1)

        end = timer()
        alltimes.append(end - start)

    return np.mean(alltimes)

# =============================================
# ================= TESTS =====================
print "======================================="
print "TESTING QUESTION 1"
print question1("cite udaciTy!", "")
# Expect True

print question1("cite udaciTy!", None)
# Expect False

print question1("cite udaciTy!", "city")
# Expect True

print question1("cite udaciTy!", "ec")
# Expect False

print question1("cite udaciTy!", "ada")
# Expect False

print "======================================="
print "TESTING QUESTION 2"
print "'" + question2("") + "'"
# Expect ''

print "'" + question2(None) + "'"
# Expect ' '

print "'" + question2(" ") + "'"
# Expect ' '

print "'" + question2("Able was I ere I saw Elba") + "'"
# Expect 'able was i ere i saw elba'

print "'" + question2("this madam likes ABBA") + "'"
# Expect ' madam '

print "'" + question2("aa") + "'"
# Expect 'aa'

print "======================================="
print "TESTING QUESTION 3"

print question3({})
# Expect {}

print question3({'A': [], 'B': [], 'C': [], 'D': [], 'E': []})
# Expect {'A': [], 'C': [], 'B': [], 'E': [], 'D': []}

print question3({'A': [('B', 0.4), ('B', 2), ("C", 1), ("D", 1.5)],
                 'B': [('A', 0.4), ("A", 2), ('C', 1.5), ("D", 1)],
                 'C': [('A', 1), ('B', 1.5), ("D", 1)],
                 "D": [('A', 1.5), ('B', 1), ("C", 1), ("E", 1)],
                 "E": [("D", 1)]})
# Expect {'A': [('B', 0.4), ('C', 1)], 'C': [('A', 1), ('D', 1)],
# 'B': [('A', 0.4)], 'E': [('D', 1)], 'D': [('C', 1), ('E', 1)]}

print "======================================="
print "TESTING QUESTION 4"

# We'll create a larger BST
root_node = 7
input_bst = np.zeros((25, 25))
input_bst[7, [6, 20]] = 1
input_bst[6, [2]] = 1
input_bst[2, [1, 4]] = 1
input_bst[4, [3, 5]] = 1
input_bst[20, [10, 21]] = 1
input_bst[10, [8, 11]] = 1
input_bst[21, [23]] = 1
input_bst[8, [9]] = 1
input_bst[11, [12]] = 1
input_bst[23, [22, 24]] = 1

print question4([], 0, 0, 0)
# Expect None

print question4([[]], 0, 1, 0)
# Expect None

print question4(input_bst, root_node, 5, 1)
# Expect 2

print question4(input_bst, root_node, 1, 5)
# Expect 2

print question4(input_bst, root_node, 12, 22)
# Expect 20

print question4(input_bst, root_node, 6, 10)
# Expect 7

print question4(input_bst, root_node, 5, 2)
# Expect 6

print "======================================="
print "TESTING QUESTION 5"

# First we create a very long linked list called example 1
example_1 = Node(6)
current_node_1 = example_1
for ii in range(6, 10000, 2):
    current_node_1.next = Node(ii)
    current_node_1 = current_node_1.next

# Now we make another linked list approximately half as long, called example 2
example_2 = Node(6)
current_node_2 = example_2
for ii in range(6, 5000, 2):
    current_node_2.next = Node(ii)
    current_node_2 = current_node_2.next

print question5(None, 1)
# Expect None

print question5(example_1, 1)
# Expect: 9998

print question5(example_2, 1)
# Expect 4998

print "Time ratio between linked lists of length 4998 and 2498:"
print time_question5(example_1) / time_question5(example_2)

print question5(Node(42), 1)
# Expect 42
