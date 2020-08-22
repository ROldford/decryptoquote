#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for SolutionTreeNode class in `decryptoquote` package."""
import pytest
from decryptoquote import decryptoquote
from typing import List


@pytest.fixture()
def solution_tree():
    coded_quote: str = "ABCD CD EF GCHICJ"
    # decoded_quote: str = "TH__ __ M_ V_OL_N" # This is my violin
    # Generate word tree for this quote
    word_tree: decryptoquote.WordTreeNode = decryptoquote.WordTreeNode()
    for word in ["THIS", "IS", "MY", "VIOLIN"]:
        word_tree.add_word(word)
    # Generate cypherletter map for this quote missing blanks
    cypherletter_map: decryptoquote.CypherLetterMap = \
        decryptoquote.CypherLetterMap()
    cypherletter_map.add_letters_to_mapping("AB", "TH")
    cypherletter_map.add_letters_to_mapping("E", "M")
    cypherletter_map.add_letters_to_mapping("GHIJ", "VOLN")
    return decryptoquote.SolutionTreeNode(coded_quote,
                                          cypherletter_map,
                                          word_tree)


def test_generate_solutions(solution_tree):
    expected_clm: decryptoquote.CypherLetterMap = decryptoquote.CypherLetterMap()
    expected_clm.add_letters_to_mapping("ABCD", "THIS")
    expected_clm.add_letters_to_mapping("CD", "IS")
    expected_clm.add_letters_to_mapping("EF", "MY")
    expected_clm.add_letters_to_mapping("GCHICJ", "VIOLIN")
    assert solution_tree.generate_solutions() == [("THIS IS MY VIOLIN",
                                                   expected_clm)]
