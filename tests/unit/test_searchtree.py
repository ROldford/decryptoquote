#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for `decryptoquote` package."""

import pytest
from anytree import Node

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

def test_initSearchTree():
    expected_values = {
        "node_name": 0,
        "ok_flag": "Maybe"
    }
    search_tree = decryptoquote.SearchTree(test_string)
    search_tree_root = search_tree.getCurrentNode()
    assert search_tree_root.name == expected_values["node_name"]
    assert isinstance(search_tree_root.puzzle, decryptoquote.Puzzle)
    assert search_tree_root.ok_flag == expected_values["ok_flag"]
