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
decoded_quote: Dict[str, List[str]] = {
    "blank": ['*****', ',', "*'*", '*', '******', '!'],
    "in_progress": ['**LL*', ',', "*'*", 'A', '**R***', '!'],
    "finished": ['HELLO', ',', "I'M", 'A', 'STRING', '!']
}
decoded_author: Dict[str, List[str]] = {
    "blank": ['****'],
    "in_progress": ['R***'],
    "finished": ['RYAN']
}
coding_dict: Dict[str, Dict[str, str]] = {
    "blank":
        {
            "A": "*", "B": "*", "C": "*", "D": "*", "E": "*",
            "F": "*", "G": "*", "H": "*", "I": "*", "J": "*",
            "K": "*", "L": "*", "M": "*", "N": "*", "O": "*",
            "P": "*", "Q": "*", "R": "*", "S": "*", "T": "*",
            "U": "*", "V": "*", "W": "*", "X": "*", "Y": "*", "Z": "*"
        },
    "in_progress":
        {
            "A": "Z", "B": "*", "C": "*", "D": "*", "E": "*",
            "F": "*", "G": "*", "H": "*", "I": "*", "J": "*",
            "K": "*", "L": "O", "M": "*", "N": "*", "O": "*",
            "P": "*", "Q": "*", "R": "I", "S": "*", "T": "*",
            "U": "*", "V": "*", "W": "*", "X": "*", "Y": "*", "Z": "*"
        },
    "finished":
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
        "author": {
            "blank": puzzle_factory.make_inital_puzzle(
                test_string,
                test_author
            ),
            "in_progress": decryptoquote.Puzzle(
                coding_dict["in_progress"],
                test_coded_quote_words,
                decoded_quote["in_progress"],
                test_coded_author_words,
                decoded_author["in_progress"]
            ),
            "finished": decryptoquote.Puzzle(
                coding_dict["finished"],
                test_coded_quote_words,
                decoded_quote["finished"],
                test_coded_author_words,
                decoded_author["finished"]
            )
        },
        "no_author": {
            "blank": puzzle_factory.make_inital_puzzle(
                test_string
            ),
            "in_progress": decryptoquote.Puzzle(
                coding_dict["in_progress"],
                test_coded_quote_words,
                decoded_quote["in_progress"]
            ),
            "finished": decryptoquote.Puzzle(
                coding_dict["finished"],
                test_coded_quote_words,
                decoded_quote["finished"]
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
    assert puzzles["author"]["blank"].coded_quote_words \
           == test_coded_quote_words
    assert puzzles["author"]["blank"].decoded_quote_words \
           == decoded_quote["blank"]
    assert puzzles["author"]["blank"].coded_author_words \
           == test_coded_author_words
    assert puzzles["author"]["blank"].decoded_author_words \
           == decoded_author["blank"]
    assert puzzles["author"]["blank"].coding_dict == coding_dict["blank"]

    assert puzzles["no_author"]["blank"].coded_quote_words \
           == test_coded_quote_words
    assert puzzles["no_author"]["blank"].decoded_quote_words \
           == decoded_quote["blank"]
    assert puzzles["no_author"]["blank"].coding_dict == coding_dict["blank"]

    assert puzzles["author"]["in_progress"].coded_quote_words \
           == test_coded_quote_words
    assert puzzles["author"]["in_progress"].decoded_quote_words \
           == decoded_quote["in_progress"]
    assert puzzles["author"]["in_progress"].coded_author_words \
           == test_coded_author_words
    assert puzzles["author"]["in_progress"].decoded_author_words \
           == decoded_author["in_progress"]
    assert puzzles["author"]["in_progress"].coding_dict \
           == coding_dict["in_progress"]

    assert puzzles["no_author"]["in_progress"].coded_quote_words \
           == test_coded_quote_words
    assert puzzles["no_author"]["in_progress"].decoded_quote_words \
           == decoded_quote["in_progress"]
    assert puzzles["no_author"]["in_progress"].coding_dict \
           == coding_dict["in_progress"]


# def test_coding_dict_is_valid(model, puzzles):
#     puzzle_wrong = decryptoquote.Puzzle(
#         test_coded_quote_words,
#         ['OELLH', ',', "I'M", 'A', 'STRINK', '!'],
#         {
#             "A": "Z", "B": "Y", "C": "X", "D": "W", "E": "V",
#             "F": "U", "G": "T", "H": "S", "I": "R", "J": "Q",
#             "K": "P", "L": "H", "M": "N", "N": "M", "O": "L",
#             "P": "G", "Q": "J", "R": "I", "S": "O", "T": "K",
#             "U": "F", "V": "E", "W": "D", "X": "C", "Y": "B", "Z": "A"
#         }
#     )
#     assert puzzles["finished"].coding_dict_is_valid(model) is True
#     assert puzzle_wrong.coding_dict_is_valid(model) is False
