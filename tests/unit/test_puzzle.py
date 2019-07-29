#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for Puzzle class in `decryptoquote` package."""

import pytest

from decryptoquote import decryptoquote

test_string = "Hello, I'm a string!"
test_coded_quote_words = ['HELLO', ',', "I'M", 'A', 'STRING', '!']
decoded = {
    "blank": ['*****', ',', "*'*", '*', '******', '!'],
    "in_progress": ['**OO*', ',', "*'*", 'Z', '**I***', '!'],
    "finished": ['SVOOL', ',', "R'N", 'Z', 'HGIRMT', '!']
}
coding_dict = {
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


@pytest.fixture
def puzzle_blank():
    return decryptoquote.Puzzle(test_string)

@pytest.fixture
def puzzle_in_progress():
    decoded_words = []
    return decryptoquote.Puzzle(
        test_coded_quote_words,
        decoded["in_progress"],
        coding_dict["in_progress"]
    )

def test_stringToCapsWords(puzzle_blank):
    input = test_string
    expected = test_coded_quote_words
    assert puzzle_blank.stringToCapsWords(input) == expected

def test_initDecodedWords(puzzle_blank):
    input = test_coded_quote_words
    expected = decoded["blank"]
    assert puzzle_blank.initDecodedWords(input) == expected

def test_initCodingDict(puzzle_blank):
    expected = coding_dict["blank"]
    assert puzzle_blank.initCodingDict() == expected

def test_initPuzzle(puzzle_blank, puzzle_in_progress):
    assert puzzle_blank.coded_words == test_coded_quote_words
    assert puzzle_blank.decoded_words == decoded["blank"]
    assert puzzle_blank.coding_dict == coding_dict["blank"]
    assert puzzle_in_progress.coded_words == test_coded_quote_words
    assert puzzle_in_progress.decoded_words == decoded["in_progress"]
    assert puzzle_in_progress.coding_dict == coding_dict["in_progress"]

def test_codingDictIsValid(puzzle_blank):
    assert True
