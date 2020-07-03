#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for functions in `decryptoquote` package."""
from typing import List, Dict

import pytest
import pyfakefs

from decryptoquote import decryptoquote


# @pytest.fixture()
# def ?():

def test_string_to_caps_words():
    assert decryptoquote.string_to_caps_words("Svool, R'n z hgirmt!") \
           == ['SVOOL', ',', "R'N", 'Z', 'HGIRMT', '!']


def test_get_blank_cypherletter_map():
    assert decryptoquote.get_blank_cypherletter_map() == {
        'A': [], 'B': [], 'C': [], 'D': [], 'E': [],
        'F': [], 'G': [], 'H': [], 'I': [], 'J': [],
        'K': [], 'L': [], 'M': [], 'N': [], 'O': [],
        'P': [], 'Q': [], 'R': [], 'S': [], 'T': [],
        'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': [],
    }


def test_add_letters_to_mapping():
    test_map: Dict[str, List[str]] = decryptoquote.get_blank_cypherletter_map()
    word: str = "ABCD"
    match: str = "THIS"
    test_map = decryptoquote.add_letters_to_mapping(test_map, word, match)
    assert test_map == {
        'A': ["T"], 'B': ["H"], 'C': ["I"], 'D': ["S"], 'E': [],
        'F': [], 'G': [], 'H': [], 'I': [], 'J': [],
        'K': [], 'L': [], 'M': [], 'N': [], 'O': [],
        'P': [], 'Q': [], 'R': [], 'S': [], 'T': [],
        'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': [],
    }
    match = "SOME"
    test_map = decryptoquote.add_letters_to_mapping(test_map, word, match)
    assert test_map == {
        'A': ["T", "S"], 'B': ["H", "O"], 'C': ["I", "M"],
        'D': ["S", "E"], 'E': [],
        'F': [], 'G': [], 'H': [], 'I': [], 'J': [],
        'K': [], 'L': [], 'M': [], 'N': [], 'O': [],
        'P': [], 'Q': [], 'R': [], 'S': [], 'T': [],
        'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': [],
    }
    match = "THEN"
    test_map = decryptoquote.add_letters_to_mapping(test_map, word, match)
    assert test_map == {
        'A': ["T", "S"], 'B': ["H", "O"], 'C': ["I", "M", "E"],
        'D': ["S", "E", "N"], 'E': [],
        'F': [], 'G': [], 'H': [], 'I': [], 'J': [],
        'K': [], 'L': [], 'M': [], 'N': [], 'O': [],
        'P': [], 'Q': [], 'R': [], 'S': [], 'T': [],
        'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': [],
    }


def test_intersect_mappings():
    # need letters where:
    #   both maps have []
    #   map_a has [] and map_b does not
    #   map_b has [] and map_a does not
    #   both have matches with no overlap
    #   both have matches with some overlap
    #   both have exact same matches
    map_a: Dict[str, List[str]] = {
        'A': [], 'B': ["Y"], 'C': ["W", "X"], 'D': ["S", "T"], 'E': ["P", "Q"],
        'F': [], 'G': [], 'H': [], 'I': [], 'J': [],
        'K': [], 'L': [], 'M': [], 'N': [], 'O': [],
        'P': [], 'Q': [], 'R': [], 'S': [], 'T': [],
        'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': [],
    }
    map_b: Dict[str, List[str]] = {
        'A': ["Z"], 'B': [], 'C': ["U", "V"], 'D': ["R", "T"], 'E': ["P", "Q"],
        'F': [], 'G': [], 'H': [], 'I': [], 'J': [],
        'K': [], 'L': [], 'M': [], 'N': [], 'O': [],
        'P': [], 'Q': [], 'R': [], 'S': [], 'T': [],
        'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': [],
    }
    expected: Dict[str, List[str]] = {
        'A': ["Z"], 'B': ["Y"], 'C': [], 'D': ["T"], 'E': ["P", "Q"],
        'F': [], 'G': [], 'H': [], 'I': [], 'J': [],
        'K': [], 'L': [], 'M': [], 'N': [], 'O': [],
        'P': [], 'Q': [], 'R': [], 'S': [], 'T': [],
        'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': [],
    }
    assert decryptoquote.intersect_mappings(map_a, map_b) == expected


def test_remove_solved_letters():
    map1: Dict[str, List[str]] = {
        'A': ["Z"], 'B': ["Z", "Y"], 'C': ["Z", "X"], 'D': [], 'E': [],
        'F': [], 'G': [], 'H': [], 'I': [], 'J': [],
        'K': [], 'L': [], 'M': [], 'N': [], 'O': [],
        'P': [], 'Q': [], 'R': [], 'S': [], 'T': [],
        'U': [], 'V': [], 'W': [], 'X': [], 'Y': ["Z", "B"], 'Z': [],
    }
    map2: Dict[str, List[str]] = {
        'A': ["Z"], 'B': [], 'C': [], 'D': [], 'E': [],
        'F': [], 'G': [], 'H': [], 'I': [], 'J': [],
        'K': [], 'L': [], 'M': [], 'N': [], 'O': [],
        'P': [], 'Q': [], 'R': [], 'S': [], 'T': [],
        'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': [],
    }
    map3: Dict[str, List[str]] = {
        'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': [], 'E': [],
        'F': [], 'G': [], 'H': [], 'I': [], 'J': [],
        'K': [], 'L': [], 'M': [], 'N': [], 'O': [],
        'P': [], 'Q': [], 'R': [], 'S': [], 'T': [],
        'U': [], 'V': [], 'W': [], 'X': [], 'Y': ["B"], 'Z': [],
    }
    map4: Dict[str, List[str]] = {
        'A': ["Z"], 'B': ["Z", "Y"], 'C': ["Y", "X"], 'D': [], 'E': [],
        'F': [], 'G': [], 'H': [], 'I': [], 'J': [],
        'K': [], 'L': [], 'M': [], 'N': [], 'O': [],
        'P': [], 'Q': [], 'R': [], 'S': [], 'T': [],
        'U': [], 'V': [], 'W': [], 'X': [], 'Y': ["X", "B"], 'Z': [],
    }
    expected1: Dict[str, List[str]] = map3
    expected2: Dict[str, List[str]] = map2
    expected3: Dict[str, List[str]] = map3
    expected4: Dict[str, List[str]] = map3
    assert decryptoquote.remove_solved_letters_from_map(map1) == expected1
    assert decryptoquote.remove_solved_letters_from_map(map2) == expected2
    assert decryptoquote.remove_solved_letters_from_map(map3) == expected3
    assert decryptoquote.remove_solved_letters_from_map(map4) == expected4


def test_decrypt_with_map():
    map1: Dict[str, List[str]] = {
        'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
        'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
        'K': ["P"], 'L': ["O"], 'M': ["N"], 'N': ["M"], 'O': ["L"],
        'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
        'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
    }
    map2: Dict[str, List[str]] = {
        'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
        'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
        'K': ["P"], 'L': ["O"], 'M': [], 'N': [], 'O': ["L"],
        'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
        'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
    }
    expected1: str = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
    expected2: str = "ZYXWVUTSRQPO__LKJIHGFEDCBA"
    assert decryptoquote.decrypt_with_cypherletter_map(decryptoquote.LETTERS,
                                                       map1) == expected1
    assert decryptoquote.decrypt_with_cypherletter_map(decryptoquote.LETTERS,
                                                       map2) == expected2


def test_get_map_as_string():
    map1: Dict[str, List[str]] = {
        'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
        'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
        'K': ["P"], 'L': ["O"], 'M': ["N"], 'N': ["M"], 'O': ["L"],
        'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
        'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
    }
    map2: Dict[str, List[str]] = {
        'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
        'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
        'K': ["P"], 'L': ["O"], 'M': [], 'N': [], 'O': ["L"],
        'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
        'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
    }
    expected1: str = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
    expected2: str = "ZYXWVUTSRQPO__LKJIHGFEDCBA"
    assert decryptoquote.get_cypherletter_map_as_string(map1) \
           == "Decoder:\n{0}\n{1}".format(decryptoquote.LETTERS, expected1)
    assert decryptoquote.get_cypherletter_map_as_string(map2) \
           == "Decoder:\n{0}\n{1}".format(decryptoquote.LETTERS, expected2)
