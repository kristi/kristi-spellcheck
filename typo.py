#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 22:09:15 2012

@author: kristi
"""

from random import randint, choice, sample, random

wordfile = "/usr/share/dict/words"
words = [line.strip().lower() for line in open(wordfile)]

num_words = len(words)

VOWEL = 'aeiouy'


def misspell(letter):
    if letter in VOWEL and random() < 0.1:
        letter = choice(VOWEL)
    if random() < 0.1:
        letter = letter.upper()
    return letter * randint(1, 3)


#for word in sample(words, 1000):
for i in xrange(5000):
    word = choice(words)
    letters = list(word)
    for i in xrange(len(letters)):
        if random() < 0.25:
            c = letters[i]
            letters[i] = misspell(c)
    print ''.join(letters)
    print word

