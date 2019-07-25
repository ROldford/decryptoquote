#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for Puzzle class in `decryptoquote` package."""

import pytest

from decryptoquote import decryptoquote

test_string = "Hello, I'm a string!"
test_coded_quote_words = ['HELLO', ',', "I'M", 'A', 'STRING', '!']
blank_plaintext_words = ['*****', ',', "*'*", '*', '******', '!']
blank_coding_dict = {
    "A": "*", "B": "*", "C": "*", "D": "*", "E": "*",
    "F": "*", "G": "*", "H": "*", "I": "*", "J": "*",
    "K": "*", "L": "*", "M": "*", "N": "*", "O": "*",
    "P": "*", "Q": "*", "R": "*", "S": "*", "T": "*",
    "U": "*", "V": "*", "W": "*", "X": "*", "Y": "*", "Z": "*"
}

@pytest.fixture
def puzzle():
    return decryptoquote.Puzzle(test_string)

def test_stringToCapsWords(puzzle):
    input = test_string
    expected = test_coded_quote_words
    assert puzzle.stringToCapsWords(input) == expected

def test_initDecodedWords(puzzle):
    input = test_coded_quote_words
    expected = blank_plaintext_words
    assert puzzle.initDecodedWords(input) == expected

def test_initCodingDict(puzzle):
    expected = blank_coding_dict
    assert puzzle.initCodingDict() == expected

def test_puzzleInit(puzzle):
    assert puzzle.coded_words == test_coded_quote_words
    assert puzzle.decoded_words == blank_plaintext_words
    assert puzzle.coding_dict == blank_coding_dict
