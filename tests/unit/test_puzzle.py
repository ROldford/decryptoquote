#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for Puzzle class in `decryptoquote` package."""
from typing import List, Dict

import pytest
import pyfakefs

from decryptoquote import decryptoquote

test_string: str = "Svool, R'n z hgirmt!"
test_coded_quote_words: List[str] = ['SVOOL', ',', "R'N", 'Z', 'HGIRMT', '!']
# TODO: turn blank, etc. string literals into constants
decoded: Dict[str, List[str]] = {
    "blank": ['*****', ',', "*'*", '*', '******', '!'],
    "in_progress": ['**LL*', ',', "*'*", 'A', '**R***', '!'],
    "finished": ['HELLO', ',', "I'M", 'A', 'STRING', '!']
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
    puzzles_dict = {
        "blank": decryptoquote.Puzzle(test_string),
        "in_progress": decryptoquote.Puzzle(
            test_coded_quote_words,
            decoded["in_progress"],
            coding_dict["in_progress"]
        ),
        "finished": decryptoquote.Puzzle(
            test_coded_quote_words,
            decoded["finished"],
            coding_dict["finished"]
        )
    }
    return puzzles_dict


@pytest.fixture()
def model(fs):
    test_corpus = "Hello, I'm a string!"
    corpus_file_path = '/test.txt'
    fs.create_file(corpus_file_path, contents=test_corpus)
    with open(corpus_file_path) as f:
        model = decryptoquote.LanguageModel(corpus_file_path)
    return model


def test_init_puzzle(puzzles):
    assert puzzles["blank"].coded_words == test_coded_quote_words
    assert puzzles["blank"].decoded_words == decoded["blank"]
    assert puzzles["blank"].coding_dict == coding_dict["blank"]
    assert puzzles["in_progress"].coded_words == test_coded_quote_words
    assert puzzles["in_progress"].decoded_words == decoded["in_progress"]
    assert puzzles["in_progress"].coding_dict == coding_dict["in_progress"]


def test_coding_dict_is_valid(model, puzzles):
    puzzle_wrong = decryptoquote.Puzzle(
        test_coded_quote_words,
        ['HELLO', ',', "I'M", 'A', 'STRINK', '!'],
        {
            "A": "Z", "B": "Y", "C": "X", "D": "W", "E": "V",
            "F": "U", "G": "T", "H": "S", "I": "R", "J": "Q",
            "K": "P", "L": "O", "M": "N", "N": "M", "O": "L",
            "P": "G", "Q": "J", "R": "I", "S": "H", "T": "K",
            "U": "F", "V": "E", "W": "D", "X": "C", "Y": "B", "Z": "A"
        }
    )
    assert puzzles["finished"].coding_dict_is_valid(model) is True
    assert puzzle_wrong.coding_dict_is_valid(model) is False
