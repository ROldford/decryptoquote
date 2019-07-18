#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for `decryptoquote` package."""

import pytest

from decryptoquote import decryptoquote

class TestUnit(object):

    def test_stringToCapsWords(self):
        input = "Hello, I'm a string!"
        expected = ['HELLO', ',', "I'M", 'A', 'STRING', '!']
        assert decryptoquote.stringToCapsWords(input) == expected

    def test_generateEmptyPlaintextWords(self):
        input = ['HELLO', ',', "I'M", 'A', 'STRING', '!']
        expected = ['*****', ',', "*'*", '*', '******', '!']
        assert decryptoquote.generateEmptyPlaintextWords(input) == expected

    def test_generateBlankCodingDictionary(self):
        expected = {
            "A": "*", "B": "*", "C": "*", "D": "*", "E": "*",
            "F": "*", "G": "*", "H": "*", "I": "*", "J": "*",
            "K": "*", "L": "*", "M": "*", "N": "*", "O": "*",
            "P": "*", "Q": "*", "R": "*", "S": "*", "T": "*",
            "U": "*", "V": "*", "W": "*", "X": "*", "Y": "*", "Z": "*"
        }
        assert decryptoquote.generateBlankCodingDictionary() == expected
