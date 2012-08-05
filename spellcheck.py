#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
spellcheck

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
    # Repeated letters are replaced with a single capital letter
    #pattern = REPEAT_RE.sub(toUpper, pattern)
    pattern = REPEAT_RE.sub(r'\1', pattern)

    return pattern


def tokenize(word):
    """
    Split word by repeated character.  Vowels get lumped together.

    >>> tokenize('hellooo')
    ['h', 'e', 'll', 'ooo']
    """
    return [m.group(0) for m in re.finditer(r'[aeiouy]+|(.)\1*', word)]


def pick_suggestion(word, candidates):
    """
    Pick best candidate word
    (word and candidates must have the same pattern)
    """
    word_tokens = tokenize(word)
    suggestion = None
    best_score = 0
    for candidate in candidates:
        candidate_tokens = tokenize(candidate)
        score = 1
        for w, c in zip(word_tokens, candidate_tokens):
            if w == c:
                score += len(c)
            elif w[0] in VOWEL and c[0] in VOWEL:
                if len(w) < len(c):
                    score = 0
                    break
                score += len(c) * (len(set(w) & set(c)) + 1)/(len(set(c)) + 1) * 0.9
            elif w[0] == c[0]:
                score += len(c) / (1 + len(w)) * 0.8
            else:
                print "score error: no match?", w, c
                score = 0
                break
        if score > best_score:
            best_score = score
            suggestion = candidate
    return suggestion


class SpellCmd(Cmd):
    def __init__(self, wordfile):
        Cmd.__init__(self)
        self.prompt = "> "
        self.intro = "Spell checker thing.  Enter some words."
        self.use_rawinput = False
        self.wordfile = wordfile

        # populate hash
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
        print word

        if word in self.words:
            print "{word} is correct".format(word=word)
        elif patt in self.approx:
            candidates = self.approx[patt]
            suggestion = pick_suggestion(word, candidates)
            if suggestion:
                print "did you mean {sugg}?".format(sugg=suggestion)
                if len(candidates) >= 2:
                    print candidates
            else:
                print "NO SUGGESTION for {word} (pattern={patt})".format(
                    word=word, patt=patt)
        else:
            print "NO SUGGESTION for {word}".format(word=word)


if __name__ == "__main__":
    #wordfile = "words.txt"
    wordfile = "/usr/share/dict/words"

    sc = SpellCmd(wordfile)
    #sc.cmdloop()
    while True:
        try:
            line = raw_input("> ")
            sc.default(line)
        except EOFError:
            break