#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for WordPatterns class in `decryptoquote` package."""
# import json
import os

import pytest
# import pyfakefs

from decryptoquote import decryptoquote

@pytest.fixture()
def word_tree():
    return decryptoquote.WordTreeNode()

def test_add_word(word_tree):
    word_tree.add_word("a")
    assert word_tree.is_word("a")
    assert word_tree.is_word("A")
    word_tree.add_word("I")
    assert word_tree.is_word("i")
    assert word_tree.is_word("I")
    word_tree.add_word("IS")
    assert word_tree.is_word("IS")
    word_tree.add_word("THIS")
    assert word_tree.is_word("THIS")
    assert not word_tree.is_word("THAT")
    word_tree.add_word("THAT")
    assert word_tree.is_word("THAT")
    word_tree.add_word("ISSUE")
    assert word_tree.is_word("ISSUE")


def test_find_words(word_tree):
    word_tree.add_word("THIS")
    word_tree.add_word("THAT")
    word_tree.add_word("THAN")
    word_tree.add_word("THEM")
    word_tree.add_word("THEN")
    word_tree.add_word("THE")
    word_tree.add_word("IS")
    word_tree.add_word("IN")
    word_tree.add_word("AN")
    word_tree.add_word("AT")
    # assert "T" in word_tree._children.keys()
    # assert "I" in word_tree._children.keys()
    # assert "A" in word_tree._children.keys()
    result_1: List[str] = word_tree.find_words("TH__")
    result_2: List[str] = word_tree.find_words("th__")
    result_3: List[str] = word_tree.find_words("THA_")
    result_4: List[str] = word_tree.find_words("TH_")
    result_5: List[str] = word_tree.find_words("I_")
    result_6: List[str] = word_tree.find_words("A_")
    result_7: List[str] = word_tree.find_words("_N")
    result_8: List[str] = word_tree.find_words("W_RD")
    assert len(result_1) == 5
    assert "THIS" in result_1
    assert "THAT" in result_1
    assert "THAN" in result_1
    assert "THEM" in result_1
    assert "THEN" in result_1
    assert len(result_2) == 5
    assert "THIS" in result_2
    assert "THAT" in result_2
    assert "THAN" in result_2
    assert "THEM" in result_2
    assert "THEN" in result_2
    assert len(result_3) == 2
    assert "THAT" in result_3
    assert "THAN" in result_3
    assert len(result_4) == 1
    assert "THE" in result_4
    assert len(result_5) == 2
    assert "IS" in result_5
    assert "IN" in result_5
    assert len(result_6) == 2
    assert "AN" in result_6
    assert "AT" in result_6
    assert len(result_7) == 2
    assert "AN" in result_7
    assert "IN" in result_7
    assert len(result_8) == 0
