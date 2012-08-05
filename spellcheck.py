#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
spellchecker

Usage:
    ./spellcheck.py

Requirements:
    Python 2.7
    Uses /usr/share/dict/words for word list

@author: kristi
"""

import re
from collections import defaultdict
from cmd import Cmd


VOWEL = set("aeiouy")
VOWEL_RE = re.compile(r'[aeiouy]')
REPEAT_RE = re.compile(r'(.)\1+')


def toPattern(word):
    def toUpper(matchobj):
        return matchobj.group(1).upper()
    pattern = word
    # Vowels get replaced with 'A'
    pattern = VOWEL_RE.sub('A', pattern)
    # Repeated letters are replaced with a single letter
    pattern = REPEAT_RE.sub(r'\1', pattern)

    return pattern


def tokenize(word):
    """
    Split word by repeated character.  Vowels get lumped together.

    >>> tokenize('oreooo')
    ['o', 'r', 'eooo']
    """
    return [m.group(0) for m in re.finditer(r'[aeiouy]+|(.)\1*', word)]


def pick_suggestion(word, candidates):
    """
    Pick best candidate word using a simple heuristic score

    Alternate scoring methodologies include:

    Python's get_close_matches string similarity via SequenceMatcher's
        Ratcliff-Obershelp based algorithm
        difflib.get_close_matches(word, candidates, n=1, cutoff=0.0)[0]
        http://docs.python.org/library/difflib.html#difflib.SequenceMatcher
        http://hg.python.org/cpython/file/70274d53c1dd/Lib/difflib.py

    Levenshtein distance or edit distance
        http://en.wikipedia.org/wiki/Levenshtein_distance

    Using a hidden markov model for each candidate
        http://en.wikipedia.org/wiki/Viterbi_algorithm
        http://en.wikipedia.org/wiki/Forward-backward_algorithm
    """
    word_tokens = tokenize(word)
    suggestion = None
    best_score = 0
    for candidate in candidates:
        candidate_tokens = tokenize(candidate)
        score = 1.0
        for w, c in zip(word_tokens, candidate_tokens):
            set_w = set(w)
            set_c = set(c)
            # Don't choose words with fewer letters
            if len(w) < len(c):
                score = 0
                break
            if w == c:
                score += len(c)
            else:
                # penalize changing vowels
                factor = (len(set_w & set_c) + 1) / (len(set_c) + 1.0)
                # small penalization for repeating letters
                factor *= 10 / (len(w) - len(c) + 10.0)
                score += factor * 0.8
        if score > best_score:
            best_score = score
            suggestion = candidate
    return suggestion


class SpellCmd(Cmd):
    def __init__(self, wordfile):
        Cmd.__init__(self)
        self.prompt = "> "
        self.intro = "Spell checker thing.  Enter some words."
        self.wordfile = wordfile

        self.words = dict.fromkeys(
            (line.strip().lower() for line in open(wordfile)), 1)

        self.approx = defaultdict(set)
        for word in self.words.iterkeys():
            pattern = toPattern(word)
            self.approx[pattern].add(word)

    def emptyline(self):
        pass

    def default(self, line):
        if line == "EOF":
            exit(0)
        word = line.strip().lower()
        patt = toPattern(word)

        if word in self.words:
            print word
        elif patt in self.approx:
            candidates = self.approx[patt]
            suggestion = pick_suggestion(word, candidates)
            if suggestion:
                print suggestion
            else:
                print "NO SUGGESTION"
        else:
            print "NO SUGGESTION"


if __name__ == "__main__":
    #wordfile = "words.txt"
    wordfile = "/usr/share/dict/words"

    sc = SpellCmd(wordfile)
    sc.cmdloop()
