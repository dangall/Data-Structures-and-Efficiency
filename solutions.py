# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 14:52:31 2017

@author: Daniele
"""

from copy import copy

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
