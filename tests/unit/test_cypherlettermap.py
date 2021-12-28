#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for CypherLetterMap in `decryptoquote` package."""
import copy
from typing import List, Dict, Optional, Tuple

import pytest

import decryptoquote.constants
from decryptoquote.cypherlettermap import CypherLetterMap


@pytest.fixture()
def cypherletter_map() -> CypherLetterMap:
    return CypherLetterMap()

@pytest.fixture()
def cypherletter_map2() -> CypherLetterMap:
    return CypherLetterMap()

@pytest.fixture()
def cypherletter_map3() -> CypherLetterMap:
    return CypherLetterMap()

@pytest.fixture()
def cypherletter_map4() -> CypherLetterMap:
    return CypherLetterMap()


def test_get_blank_cypherletter_map(cypherletter_map):
    for letter in decryptoquote.constants.LETTERS:
        assert cypherletter_map.get_letter_for_cypher(letter) is None


def test_add_word_to_mapping(cypherletter_map):
    word: str = "abcd"
    match = "this"
    others: str = "EFGHIJKLMNOPQRSTUVWXYZ"
    cypherletter_map = word_add_case(cypherletter_map, word, match, others)
    word = "EFG"
    match = "ONE"
    others = others[3:]
    cypherletter_map = word_add_case(cypherletter_map, word, match, others)
    word = "HEIJD"
    match = "wOrKs"
    others = others[3:]
    cypherletter_map = word_add_case(cypherletter_map, word, match, others)


def word_add_case(
    cypherletter_map: CypherLetterMap,
    word: str,
    match: str,
    others: str
) -> CypherLetterMap:
    cypherletter_map.add_word_to_mapping(word, match)
    for letter_pair in zip(word.upper(), match.upper()):
        coded, decoded = letter_pair
        assert cypherletter_map.get_letter_for_cypher(coded) == decoded
    for letter in others.upper():
        assert cypherletter_map.get_letter_for_cypher(letter) is None
    return cypherletter_map



def test_add_word_to_mapping_exceptions(cypherletter_map):
    with pytest.raises(ValueError) as e:
        cypherletter_map.add_word_to_mapping("ABC", "THIS")
    assert str(e.value) == "Coded and decoded words must have the same length"
    word: str = "ABCD"
    match = "THIS"
    cypherletter_map.add_word_to_mapping(word, match)
    word = "CD"
    match = "AT"
    with pytest.raises(ValueError) as e:
        cypherletter_map.add_word_to_mapping(word, match)
    assert str(e.value) == f"Coded letter {word[0]} already has a match"
    assert cypherletter_map.get_letter_for_cypher("E") is None
    assert cypherletter_map.get_letter_for_cypher("C") == "I"
    assert cypherletter_map.get_letter_for_cypher("D") == "S"
    word = "EF"
    match = "IS"
    with pytest.raises(ValueError) as e:
        cypherletter_map.add_word_to_mapping(word, match)
    assert str(e.value) == f"Decoded letter {match[0]} is already mapped to " \
                           f"another coded letter"
    assert cypherletter_map.get_letter_for_cypher("E") is None
    assert cypherletter_map.get_letter_for_cypher("F") is None
    assert cypherletter_map.get_letter_for_cypher("C") == "I"
    assert cypherletter_map.get_letter_for_cypher("D") == "S"


def test_add_letters_to_map_punctuation(cypherletter_map):
    word: str = "!"
    match = "!"
    cypherletter_map.add_word_to_mapping(word, match)
    for letter in decryptoquote.constants.LETTERS:
        assert cypherletter_map.get_letter_for_cypher(letter) is None
    word = "A'"
    match = "'B"
    with pytest.raises(ValueError) as e:
        cypherletter_map.add_word_to_mapping(word, match)
    assert str(e.value) == f"Coded word {word} and decoded word {match} have " \
                           f"different punctuation locations"


def test_remove_word_from_mapping(cypherletter_map):
    others: str = "EFGHIJKLMNOPQRSTUVWXYZ"
    word: str = "abcd"
    match = "this"
    cypherletter_map.add_word_to_mapping(word, match)
    word = "EFG"
    match = "ONE"
    cypherletter_map.add_word_to_mapping(word, match)
    assert cypherletter_map.get_letter_for_cypher("E") == "O"
    assert cypherletter_map.get_letter_for_cypher("F") == "N"
    assert cypherletter_map.get_letter_for_cypher("G") == "E"
    for letter in others[3:]:
        assert cypherletter_map.get_letter_for_cypher(letter) is None
    cypherletter_map.remove_last_word_from_mapping()
    assert cypherletter_map.get_letter_for_cypher("E") is None
    assert cypherletter_map.get_letter_for_cypher("F") is None
    assert cypherletter_map.get_letter_for_cypher("G") is None
    for letter in others[3:]:
        assert cypherletter_map.get_letter_for_cypher(letter) is None
    cypherletter_map.remove_last_word_from_mapping()
    for letter in decryptoquote.constants.LETTERS:
        assert cypherletter_map.get_letter_for_cypher(letter) is None


def test_clear(cypherletter_map):
    others = decryptoquote.constants.LETTERS
    for letter in others:
        assert cypherletter_map.get_letter_for_cypher(letter) is None
    cypherletter_map = word_add_case(
        cypherletter_map, "ABCD", "THIS", others[4:])
    cypherletter_map.clear()
    for letter in others:
        assert cypherletter_map.get_letter_for_cypher(letter) is None


def test_does_word_coding_work(cypherletter_map):
    word: str = "abcd"
    match = "this"
    cypherletter_map.add_word_to_mapping(word, match)
    # works
    word_coding_case(cypherletter_map, "efg", "one", True)  # all new
    word_coding_case(cypherletter_map, "cd", "is", True)  # old matches
    word_coding_case(cypherletter_map, "'.", "'.", True)  # good punctuation
    # doesn't work
    word_coding_case(cypherletter_map, "cd", "it", False)  # bad remap
    word_coding_case(cypherletter_map, "efg", "two", False)  # double t
    word_coding_case(cypherletter_map, "ef", "one", False)  # bad length
    word_coding_case(cypherletter_map, "'.", ".'", False)  # punct mismatch
    word_coding_case(cypherletter_map, "'.", "is", False)  # punct mismatch
    word_coding_case(cypherletter_map, "ef", ".'", False)  # punct mismatch


def word_coding_case(
    cypherletter_map,
    coded_word: str,
    possible_decoded_word: str,
    expected: bool
):
    mapping_works = cypherletter_map.does_word_coding_work(
        coded_word, possible_decoded_word)
    assert mapping_works == expected


def test_decode_with_map(cypherletter_map,
                         cypherletter_map2,
                         cypherletter_map3):
    # map1: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
    #     'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
    #     'K': ["P"], 'L': ["O"], 'M': ["N"], 'N': ["M"], 'O': ["L"],
    #     'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
    #     'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
    # }
    cypherletter_map.add_word_to_mapping("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                                "ZYXWVUTSRQPONMLKJIHGFEDCBA")
    # map2: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
    #     'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
    #     'K': ["P"], 'L': ["M", "N"], 'M': ["L", "N"], 'N': ["L", "M"],
    #     'O': ["L"],
    #     'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
    #     'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
    # }
    cypherletter_map2.add_word_to_mapping("ABCDEFGHIJK", "ZYXWVUTSRQP")
    cypherletter_map2.add_word_to_mapping("OPQRSTUVWXYZ", "LKJIHGFEDCBA")
    # map3: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': None, 'C': None, 'D': None, 'E': None,
    #     'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
    #     'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
    #     'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
    #     'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': ["A"],
    # }
    cypherletter_map3.add_word_to_mapping("AZ", "ZA")
    expected1: str = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
    expected2: str = "ZYXWVUTSRQP___LKJIHGFEDCBA"
    expected3: str = "Z________________________A"
    assert cypherletter_map.decode(decryptoquote.constants.LETTERS) == expected1
    assert cypherletter_map2.decode(
        decryptoquote.constants.LETTERS) == expected2
    assert cypherletter_map3.decode(
        decryptoquote.constants.LETTERS) == expected3


def test_str(cypherletter_map, cypherletter_map2, cypherletter_map3):
    cypherletter_map.add_word_to_mapping(decryptoquote.constants.LETTERS,
                                            "ZYXWVUTSRQPONMLKJIHGFEDCBA")
    # map1: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
    #     'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
    #     'K': ["P"], 'L': ["O"], 'M': ["N"], 'N': ["M"], 'O': ["L"],
    #     'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
    #     'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
    # }
    cypherletter_map3.add_word_to_mapping("AZ", "ZA")
    # map3: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': None, 'C': None, 'D': None, 'E': None,
    #     'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
    #     'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
    #     'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
    #     'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': ["A"],
    # }
    expected1: str = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
    expected3: str = "Z________________________A"
    assert str(cypherletter_map) \
           == "Decoder:\n{0}\n{1}".format(decryptoquote.constants.LETTERS, expected1)
    assert str(cypherletter_map3) \
           == "Decoder:\n{0}\n{1}".format(decryptoquote.constants.LETTERS, expected3)


def test_repr(cypherletter_map, cypherletter_map2, cypherletter_map3):
    cypherletter_map.add_word_to_mapping(decryptoquote.constants.LETTERS,
                                            "ZYXWVUTSRQPONMLKJIHGFEDCBA")
    # map1: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
    #     'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
    #     'K': ["P"], 'L': ["O"], 'M': ["N"], 'N': ["M"], 'O': ["L"],
    #     'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
    #     'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
    # }
    cypherletter_map3.add_word_to_mapping("AZ", "ZA")
    # map3: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': None, 'C': None, 'D': None, 'E': None,
    #     'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
    #     'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
    #     'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
    #     'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': ["A"],
    # }
    expected1: str = "{'A': 'Z', 'B': 'Y', 'C': 'X', 'D': 'W', 'E': 'V', " \
                     "'F': 'U', 'G': 'T', 'H': 'S', 'I': 'R', " \
                     "'J': 'Q', 'K': 'P', 'L': 'O', 'M': 'N', " \
                     "'N': 'M', 'O': 'L', 'P': 'K', 'Q': 'J', " \
                     "'R': 'I', 'S': 'H', 'T': 'G', 'U': 'F', " \
                     "'V': 'E', 'W': 'D', 'X': 'C', 'Y': 'B', " \
                     "'Z': 'A'}"
    expected3: str = "{'A': 'Z', 'B': None, 'C': None, 'D': None, 'E': None, " \
                     "'F': None, 'G': None, 'H': None, 'I': None, " \
                     "'J': None, 'K': None, 'L': None, 'M': None, 'N': None, " \
                     "'O': None, 'P': None, 'Q': None, 'R': None, 'S': None, " \
                     "'T': None, 'U': None, 'V': None, 'W': None, 'X': None, " \
                     "'Y': None, 'Z': 'A'}"
    assert repr(cypherletter_map) \
           == "CypherLetterMap({0})".format(expected1)
    assert repr(cypherletter_map3) \
           == "CypherLetterMap({0})".format(expected3)


def test_eq(cypherletter_map,
            cypherletter_map2,
            cypherletter_map3,
            cypherletter_map4):
    cypherletter_map.add_word_to_mapping("ABCD", "SELF")
    cypherletter_map2.add_word_to_mapping("ABCDE", "OTHER")
    cypherletter_map3.add_word_to_mapping("ABCD", "SELF")
    not_a_clm: str = "not a cypherletter map"
    assert cypherletter_map == cypherletter_map
    assert cypherletter_map == cypherletter_map3
    assert cypherletter_map != cypherletter_map2
    assert cypherletter_map != not_a_clm


def test_deepcopy(cypherletter_map):
    cypherletter_map2 = copy.deepcopy(cypherletter_map)
    cypherletter_map.add_word_to_mapping("ABCDEF", "CHANGE")
    assert cypherletter_map != cypherletter_map2
