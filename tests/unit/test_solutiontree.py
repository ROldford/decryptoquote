#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for SolutionTreeNode class in `decryptoquote` package."""
import pytest
from decryptoquote import decryptoquote
from typing import List


@pytest.fixture()
def word_tree():
    coded_quote: str = "ABCD CD EF GCHICJ"
    decoded_quote: str = "TH__ __ M_ V_OL_N"

    return decryptoquote.WordTreeNode()


def test_add_word(word_tree):
