# Spellcheck

## `./spellcheck.py`
Runs an interactive prompt where you enter a word and the script
prints out the corrected word (or "NO SUGGESTION" if no correction
could be found).

Example session

    ./spellcheck.py
    > shEEEEEEEEEp
    sheep
    > peepple
    people
    > sheeple
    NO SUGGESTION

Spelling errors may be
* Case errors: `inSIDE` => `inside`
* Repeated letters: `jjoobbb` => `job`
* Incorrect vowels: `weke` => `wake`

Any combination of errors are corrected (e.g. `CUNsperrICY` => `conspiracy`)

## `./typo.py`
Generates words with spelling errors.

The output of `./typo.py` can be piped into `./spellcheck.py`, and verified that no occurrences of "NO SUGGESTION" appear

    ./typo.py | ./spellcheck.py | grep "NO SUGGESTION"

## Requirements
* Python 2.7 (earlier python versions may work but weren't tested)
* *nix `/usr/share/dict/words` file

## Details
This spellcheck solution is O(1) per word checked because it makes two hash lookups: first to find an exact word match, and a second hash lookup to determine if the input is a correctible spelling pattern.

If there are multiple possible corrections, this program calculates a simple score to determine the best word.

## Original Specification
Write a program that reads a large list of English words (e.g. from /usr/share/dict/words on a unix system) into memory, and then reads words from stdin, and prints either the best spelling suggestion, or "NO SUGGESTION" if no suggestion can be found. The program should print ">" as a prompt before reading each word, and should loop until killed.

Your solution should be faster than O(n) per word checked, where n is the length of the dictionary. That is to say, you can't scan the dictionary every time you want to spellcheck a word.

For example:

    > sheeeeep
    sheep
    > peepple
    people
    > sheeple
    NO SUGGESTION

The class of spelling mistakes to be corrected is as follows:

* Case (upper/lower) errors: "inSIDE" => "inside"
* Repeated letters: "jjoobbb" => "job"
* Incorrect vowels: "weke" => "wake"

Any combination of the above types of error in a single word should be corrected (e.g. "CUNsperrICY" => "conspiracy").

If there are many possible corrections of an input word, your program can choose one in any way you like. It just has to be an English word that is a spelling correction of the input by the above rules.

Final step: Write a second program that *generates* words with spelling mistakes of the above form, starting with correctly spelled English words. Pipe its output into the first program and verify that there are no occurrences of "NO SUGGESTION" in the output.
