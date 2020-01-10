#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for Puzzle class in `decryptoquote` package."""
from typing import List, Dict

import pytest
import pyfakefs

from decryptoquote import decryptoquote

test_string: str = "Svool, R'n z hgirmt!"
test_coded_quote_words: List[str] = ['SVOOL', ',', "R'N", 'Z', 'HGIRMT', '!']
test_author: str = "Ibzm"
test_coded_author_words: List[str] = ['IBZM']
# TODO: turn blank, etc. string literals into constants
BLANK = "blank"
IN_PROGRESS = "in_progress"
FINISHED = "finished"
AUTHOR = "author"
NO_AUTHOR = "no-author"
decoded_quote: Dict[str, List[str]] = {
    BLANK: ['*****', ',', "*'*", '*', '******', '!'],
    IN_PROGRESS: ['**LL*', ',', "*'*", 'A', '**R***', '!'],
    FINISHED: ['HELLO', ',', "I'M", 'A', 'STRING', '!']
}
decoded_author: Dict[str, List[str]] = {
    BLANK: ['****'],
    IN_PROGRESS: ['R***'],
    FINISHED: ['RYAN']
}
coding_dict: Dict[str, Dict[str, str]] = {
    BLANK:
        {
            "A": "*", "B": "*", "C": "*", "D": "*", "E": "*",
            "F": "*", "G": "*", "H": "*", "I": "*", "J": "*",
            "K": "*", "L": "*", "M": "*", "N": "*", "O": "*",
            "P": "*", "Q": "*", "R": "*", "S": "*", "T": "*",
            "U": "*", "V": "*", "W": "*", "X": "*", "Y": "*", "Z": "*"
        },
    IN_PROGRESS:
        {
            "A": "Z", "B": "*", "C": "*", "D": "*", "E": "*",
            "F": "*", "G": "*", "H": "*", "I": "*", "J": "*",
            "K": "*", "L": "O", "M": "*", "N": "*", "O": "*",
            "P": "*", "Q": "*", "R": "I", "S": "*", "T": "*",
            "U": "*", "V": "*", "W": "*", "X": "*", "Y": "*", "Z": "*"
        },
    FINISHED:
        {
            "A": "Z", "B": "Y", "C": "X", "D": "W", "E": "V",
            "F": "U", "G": "T", "H": "S", "I": "R", "J": "Q",
            "K": "P", "L": "O", "M": "N", "N": "M", "O": "L",
            "P": "K", "Q": "J", "R": "I", "S": "H", "T": "G",
            "U": "F", "V": "E", "W": "D", "X": "C", "Y": "B", "Z": "A"
        }
}


@pytest.fixture()
def puzzles():
    puzzle_factory = decryptoquote.PuzzleTree()
    puzzles_dict = {
        AUTHOR: {
            BLANK: puzzle_factory.make_inital_puzzle(
                test_string,
                test_author
            ),
            IN_PROGRESS: decryptoquote.Puzzle(
                coding_dict[IN_PROGRESS],
                test_coded_quote_words,
                decoded_quote[IN_PROGRESS],
                test_coded_author_words,
                decoded_author[IN_PROGRESS]
            ),
            FINISHED: decryptoquote.Puzzle(
                coding_dict[FINISHED],
                test_coded_quote_words,
                decoded_quote[FINISHED],
                test_coded_author_words,
                decoded_author[FINISHED]
            )
        },
        NO_AUTHOR: {
            BLANK: puzzle_factory.make_inital_puzzle(
                test_string
            ),
            IN_PROGRESS: decryptoquote.Puzzle(
                coding_dict[IN_PROGRESS],
                test_coded_quote_words,
                decoded_quote[IN_PROGRESS]
            ),
            FINISHED: decryptoquote.Puzzle(
                coding_dict[FINISHED],
                test_coded_quote_words,
                decoded_quote[FINISHED]
            )
        }
    }
    return puzzles_dict


@pytest.fixture()
def model(fs):
    test_corpus = "Hello, I'm a string!"
    corpus_file_path = '/test.txt'
    fs.create_file(corpus_file_path, contents=test_corpus)
    # TODO: remove file open
    with open(corpus_file_path) as f:
        model = decryptoquote.LanguageModel(corpus_file_path)
    return decryptoquote.LanguageModel(corpus_file_path)


def test_init_puzzle(puzzles):
    assert puzzles[AUTHOR][BLANK].coded_quote_words \
           == test_coded_quote_words
    assert puzzles[AUTHOR][BLANK].decoded_quote_words \
           == decoded_quote[BLANK]
    assert puzzles[AUTHOR][BLANK].coded_author_words \
           == test_coded_author_words
    assert puzzles[AUTHOR][BLANK].decoded_author_words \
           == decoded_author[BLANK]
    assert puzzles[AUTHOR][BLANK].coding_dict \
           == coding_dict[BLANK]

    assert puzzles[NO_AUTHOR][BLANK].coded_quote_words \
           == test_coded_quote_words
    assert puzzles[NO_AUTHOR][BLANK].decoded_quote_words \
           == decoded_quote[BLANK]
    assert puzzles[NO_AUTHOR][BLANK].coding_dict \
           == coding_dict[BLANK]

    assert puzzles[AUTHOR][IN_PROGRESS].coded_quote_words \
           == test_coded_quote_words
    assert puzzles[AUTHOR][IN_PROGRESS].decoded_quote_words \
           == decoded_quote[IN_PROGRESS]
    assert puzzles[AUTHOR][IN_PROGRESS].coded_author_words \
           == test_coded_author_words
    assert puzzles[AUTHOR][IN_PROGRESS].decoded_author_words \
           == decoded_author[IN_PROGRESS]
    assert puzzles[AUTHOR][IN_PROGRESS].coding_dict \
           == coding_dict[IN_PROGRESS]

    assert puzzles[NO_AUTHOR][IN_PROGRESS].coded_quote_words \
           == test_coded_quote_words
    assert puzzles[NO_AUTHOR][IN_PROGRESS].decoded_quote_words \
           == decoded_quote[IN_PROGRESS]
    assert puzzles[NO_AUTHOR][IN_PROGRESS].coding_dict \
           == coding_dict[IN_PROGRESS]

def test_is_solved(puzzles):
    assert puzzles[AUTHOR][BLANK].is_solved() is False
    assert puzzles[AUTHOR][IN_PROGRESS].is_solved() is False
    assert puzzles[AUTHOR][FINISHED].is_solved() is True
    assert puzzles[NO_AUTHOR][BLANK].is_solved() is False
    assert puzzles[NO_AUTHOR][IN_PROGRESS].is_solved() is False
    assert puzzles[NO_AUTHOR][FINISHED].is_solved() is True

def test_get_solution_string(puzzles):
    assert puzzles[AUTHOR][FINISHED].get_solution_string() \
           == "HELLO, I'M A STRING! - RYAN"
    assert puzzles[NO_AUTHOR][FINISHED].get_solution_string() \
           == "HELLO, I'M A STRING!"
