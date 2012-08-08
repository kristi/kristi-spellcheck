#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generates misspelled words where misspellings can be:
    * Upper case letters
    * Repeated letters
    * Wrong vowel

Usage:
    ./typo.py

    ./typo.py | ./spellcheck.py | grep "NO SUGGESTION"

Requirements:
    Python 2.7
    Uses /usr/share/dict/words for word list

@author: kristi
"""

from random import randint, choice, random

wordfile = "/usr/share/dict/words"
words = [line.strip().lower() for line in open(wordfile)]

num_words = len(words)

VOWEL = 'aeiouy'


def misspell(letter):
    if letter in VOWEL and random() < 0.5:
        letter = choice(VOWEL)
    if random() < 0.2:
        letter = letter.upper()
    return letter * randint(1, 4)


if __name__ == "__main__":
    for i in xrange(5000):
        word = choice(words)
        letters = list(word)
        for i in xrange(len(letters)):
            if random() < 0.3:
                c = letters[i]
                letters[i] = misspell(c)
        print ''.join(letters)
        print word
