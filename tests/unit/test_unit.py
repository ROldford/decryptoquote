#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for `decryptoquote` package."""

import pytest
from anytree import Node, RenderTree

from decryptoquote import decryptoquote

class TestUnit(object):

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

    def test_stringToCapsWords(self):
        input = self.test_string
        expected = self.test_coded_quote_words
        assert decryptoquote.stringToCapsWords(input) == expected

    def test_generateEmptyPlaintextWords(self):
        input = self.test_coded_quote_words
        expected = self.blank_plaintext_words
        assert decryptoquote.generateEmptyPlaintextWords(input) == expected

    def test_generateBlankCodingDictionary(self):
        expected = self.blank_coding_dict
        assert decryptoquote.generateBlankCodingDictionary() == expected

    def test_generateSearchTree(self):
        expected_root_node = Node(
            "0",
            coding_dict=self.blank_coding_dict,
            plaintext_words=self.blank_plaintext_words,
            ok_flag = "Maybe")
        output = decryptoquote.generateSearchTree(self.test_coded_quote_words)
        assert output.name == expected_root_node.name
        assert output.coding_dict == expected_root_node.coding_dict
        assert output.plaintext_words == expected_root_node.plaintext_words
        assert output.ok_flag == expected_root_node.ok_flag
