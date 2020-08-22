#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for CypherLetterMap in `decryptoquote` package."""
import copy
from typing import List, Dict, Optional, Tuple

import pytest

from decryptoquote import decryptoquote


@pytest.fixture()
def cypherletter_map() -> decryptoquote.CypherLetterMap:
    return decryptoquote.CypherLetterMap()

@pytest.fixture()
def cypherletter_map2() -> decryptoquote.CypherLetterMap:
    return decryptoquote.CypherLetterMap()

@pytest.fixture()
def cypherletter_map3() -> decryptoquote.CypherLetterMap:
    return decryptoquote.CypherLetterMap()

@pytest.fixture()
def cypherletter_map4() -> decryptoquote.CypherLetterMap:
    return decryptoquote.CypherLetterMap()


def test_get_blank_cypherletter_map(cypherletter_map):
    for letter in decryptoquote.LETTERS:
        assert cypherletter_map.get_letter_for_cypher(letter) is None


def test_add_letters_to_mapping(cypherletter_map):
    others: str = "EFGHIJKLMNOPQRSTUVWXYZ"
    word: str = "ABCD"
    match: str = "THIS"
    cypherletter_map.add_letters_to_mapping(word, match)
    assert cypherletter_map.get_letter_for_cypher("A") == ["T"]
    assert cypherletter_map.get_letter_for_cypher("B") == ["H"]
    assert cypherletter_map.get_letter_for_cypher("C") == ["I"]
    assert cypherletter_map.get_letter_for_cypher("D") == ["S"]
    for letter in others:
        assert cypherletter_map.get_letter_for_cypher(letter) == None
    match = "SOME"
    cypherletter_map.add_letters_to_mapping(word, match)
    assert cypherletter_map.get_letter_for_cypher("A") == ["T", "S"]
    assert cypherletter_map.get_letter_for_cypher("B") == ["H", "O"]
    assert cypherletter_map.get_letter_for_cypher("C") == ["I", "M"]
    assert cypherletter_map.get_letter_for_cypher("D") == ["S", "E"]
    for letter in others:
        assert cypherletter_map.get_letter_for_cypher(letter) == None
    match = "THEN"
    cypherletter_map.add_letters_to_mapping(word, match)
    assert cypherletter_map.get_letter_for_cypher("A") == ["T", "S"]
    assert cypherletter_map.get_letter_for_cypher("B") == ["H", "O"]
    assert cypherletter_map.get_letter_for_cypher("C") == ["I", "M", "E"]
    assert cypherletter_map.get_letter_for_cypher("D") == ["S", "E", "N"]
    for letter in others:
        assert cypherletter_map.get_letter_for_cypher(letter) == None


def test_add_letters_to_map_punctuation(cypherletter_map):
    word: str = "!"
    match: str = "!"
    cypherletter_map.add_letters_to_mapping(word, match)
    for letter in decryptoquote.LETTERS:
        assert cypherletter_map.get_letter_for_cypher(letter) == None


def test_decrypt_with_map(cypherletter_map,
                          cypherletter_map2,
                          cypherletter_map3):
    # map1: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
    #     'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
    #     'K': ["P"], 'L': ["O"], 'M': ["N"], 'N': ["M"], 'O': ["L"],
    #     'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
    #     'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
    # }
    cypherletter_map.add_letters_to_mapping("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                                "ZYXWVUTSRQPONMLKJIHGFEDCBA")
    # map2: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
    #     'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
    #     'K': ["P"], 'L': ["M", "N"], 'M': ["L", "N"], 'N': ["L", "M"],
    #     'O': ["L"],
    #     'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
    #     'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
    # }
    cypherletter_map2.add_letters_to_mapping("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                                "ZYXWVUTSRQPMLLLKJIHGFEDCBA")
    cypherletter_map2.add_letters_to_mapping("LMN", "NNM")
    # map3: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': None, 'C': None, 'D': None, 'E': None,
    #     'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
    #     'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
    #     'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
    #     'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': ["A"],
    # }
    cypherletter_map3.add_letters_to_mapping("AZ", "ZA")
    expected1: str = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
    expected2: str = "ZYXWVUTSRQP___LKJIHGFEDCBA"
    expected3: str = "Z________________________A"
    assert decryptoquote.decrypt_with_cypherletter_map(
        decryptoquote.LETTERS,
        cypherletter_map) == expected1
    assert decryptoquote.decrypt_with_cypherletter_map(
        decryptoquote.LETTERS,
        cypherletter_map2) == expected2
    assert decryptoquote.decrypt_with_cypherletter_map(
        decryptoquote.LETTERS,
        cypherletter_map3) == expected3


def test_intersect_mappings(cypherletter_map, cypherletter_map2):
    # need letters where:
    #   both maps have []
    #   map_a has [] and map_b does not
    #   map_b has [] and map_a does not
    #   both have matches with no overlap
    #   both have matches with some overlap
    #   both have exact same matches
    cypherletter_map.add_letters_to_mapping("BDE", "YSP")
    cypherletter_map.add_letters_to_mapping("DE", "TQ")
    # map_a: Dict[str, Optional[List[str]]] = {
    #     'A': None, 'B': ["Y"], 'C': None, 'D': ["S", "T"],
    #     'E': ["P", "Q"],
    #     'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
    #     'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
    #     'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
    #     'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': None,
    # }
    cypherletter_map2.add_letters_to_mapping("ADE", "ZRP")
    cypherletter_map2.add_letters_to_mapping("DE", "TQ")
    # map_b: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': None, 'C': None, 'D': ["R", "T"],
    #     'E': ["P", "Q"],
    #     'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
    #     'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
    #     'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
    #     'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': None,
    # }
    cypherletter_map.intersect_mappings(cypherletter_map2)
    assert cypherletter_map.get_letter_for_cypher('A') == ["Z"]
    assert cypherletter_map.get_letter_for_cypher('B') == ["Y"]
    assert cypherletter_map.get_letter_for_cypher('D') == ["T"]
    assert cypherletter_map.get_letter_for_cypher('E') == ["P", "Q"]
    for letter in "CFGHIJKLMNOPQRSTUVWXYZ":
        assert cypherletter_map.get_letter_for_cypher(letter) == None
    # expected: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': ["Y"], 'C': None, 'D': ["T"], 'E': ["P", "Q"],
    #     'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
    #     'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
    #     'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
    #     'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': None,
    # }

def test_intersect_mappings_exception(cypherletter_map, cypherletter_map2):
    cypherletter_map.add_letters_to_mapping("A", "Z")
    cypherletter_map2.add_letters_to_mapping("A", "Y")
    with pytest.raises(ValueError) as except_info:
        cypherletter_map.intersect_mappings(cypherletter_map2)
    assert "A code letter was left with no possible solution" \
           in str(except_info.value)


def test_remove_solved_letters(cypherletter_map,
                               cypherletter_map2,
                               cypherletter_map3,
                               cypherletter_map4):
    # map1: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': ["Z", "Y"], 'C': ["Z", "X"], 'D': None, 'E': None,
    #     'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
    #     'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
    #     'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
    #     'U': None, 'V': None, 'W': None, 'X': None, 'Y': ["Z", "B"], 'Z': None,
    # }
    cypherletter_map.add_letters_to_mapping("ABCY", "ZZZZ")
    cypherletter_map.add_letters_to_mapping("BCY", "YXB")
    # map2: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': None, 'C': None, 'D': None, 'E': None,
    #     'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
    #     'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
    #     'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
    #     'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': None,
    # }
    cypherletter_map2.add_letters_to_mapping("A", "Z")
    # map3: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': None, 'E': None,
    #     'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
    #     'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
    #     'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
    #     'U': None, 'V': None, 'W': None, 'X': None, 'Y': ["B"], 'Z': None,
    # }
    cypherletter_map3.add_letters_to_mapping("ABCY", "ZYXB")
    # map4: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': ["Z", "Y"], 'C': ["Y", "X"], 'D': None, 'E': None,
    #     'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
    #     'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
    #     'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
    #     'U': None, 'V': None, 'W': None, 'X': None, 'Y': ["X", "B"], 'Z': None,
    # }
    cypherletter_map4.add_letters_to_mapping("ABCY", "ZZYX")
    cypherletter_map4.add_letters_to_mapping("BCY", "YXB")
    # actual1: Dict[str, Optional[List[str]]] = \
    #     decryptoquote.remove_solved_letters_from_map(map1)
    # actual2: Dict[str, Optional[List[str]]] = \
    #     decryptoquote.remove_solved_letters_from_map(map2)
    # actual3: Dict[str, Optional[List[str]]] = \
    #     decryptoquote.remove_solved_letters_from_map(map3)
    # actual4: Dict[str, Optional[List[str]]] = \
    #     decryptoquote.remove_solved_letters_from_map(map4)
    cypherletter_map.remove_solved_letters_from_map()
    cypherletter_map2.remove_solved_letters_from_map()
    cypherletter_map3.remove_solved_letters_from_map()
    cypherletter_map4.remove_solved_letters_from_map()
    match_list1: List[Tuple[str, str]] = [("A", "Z"),
                                          ("B", "Y"),
                                          ("C", "X"),
                                          ("Y", "B")]
    match_list2: List[Tuple[str, str]] = [("A", "Z")]
    remove_solved_letters_case(cypherletter_map, match_list1, 4)
    remove_solved_letters_case(cypherletter_map2, match_list2, 1)
    remove_solved_letters_case(cypherletter_map3, match_list1, 4)
    remove_solved_letters_case(cypherletter_map4, match_list1, 4)


def remove_solved_letters_case(clmap: decryptoquote.CypherLetterMap,
                               expected_matches: List[Tuple[str, str]],
                               solved_count: int) -> None:
    for match_pair in expected_matches:
        letter, match = match_pair
        assert clmap.get_letter_for_cypher(letter) == [match]
    assert len(clmap.get_letter_for_cypher("D")) == 26 - (solved_count + 1)


def test_remove_solved_letters_exception(cypherletter_map):
    # map1: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': ["Z"], 'C': None, 'D': None, 'E': None,
    #     'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
    #     'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
    #     'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
    #     'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': None,
    # }
    cypherletter_map.add_letters_to_mapping("AB", "ZZ")
    with pytest.raises(ValueError) as except_info:
        cypherletter_map.remove_solved_letters_from_map()
    assert "A code letter was left with no possible solution" \
           in str(except_info.value)


def test_str(cypherletter_map, cypherletter_map2, cypherletter_map3):
    cypherletter_map.add_letters_to_mapping(decryptoquote.LETTERS,
                                            "ZYXWVUTSRQPONMLKJIHGFEDCBA")
    # map1: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
    #     'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
    #     'K': ["P"], 'L': ["O"], 'M': ["N"], 'N': ["M"], 'O': ["L"],
    #     'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
    #     'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
    # }
    cypherletter_map2.add_letters_to_mapping(decryptoquote.LETTERS,
                                             "ZYXWVUTSRQPMLLLKJIHGFEDCBA")
    cypherletter_map2.add_letters_to_mapping("LMN", "NNM")
    # map2: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
    #     'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
    #     'K': ["P"], 'L': ["M", "N"], 'M': ["L", "N"], 'N': ["L", "M"], 'O': ["L"],
    #     'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
    #     'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
    # }
    cypherletter_map3.add_letters_to_mapping("AZ", "ZA")
    # map3: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': None, 'C': None, 'D': None, 'E': None,
    #     'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
    #     'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
    #     'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
    #     'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': ["A"],
    # }
    print(repr(cypherletter_map))
    expected1: str = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
    expected2: str = "ZYXWVUTSRQP___LKJIHGFEDCBA"
    expected3: str = "Z________________________A"
    assert str(cypherletter_map) \
           == "Decoder:\n{0}\n{1}".format(decryptoquote.LETTERS, expected1)
    assert str(cypherletter_map2) \
           == "Decoder:\n{0}\n{1}".format(decryptoquote.LETTERS, expected2)
    assert str(cypherletter_map3) \
           == "Decoder:\n{0}\n{1}".format(decryptoquote.LETTERS, expected3)


def test_repr(cypherletter_map, cypherletter_map2, cypherletter_map3):
    cypherletter_map.add_letters_to_mapping(decryptoquote.LETTERS,
                                            "ZYXWVUTSRQPONMLKJIHGFEDCBA")
    # map1: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
    #     'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
    #     'K': ["P"], 'L': ["O"], 'M': ["N"], 'N': ["M"], 'O': ["L"],
    #     'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
    #     'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
    # }
    cypherletter_map2.add_letters_to_mapping(decryptoquote.LETTERS,
                                             "ZYXWVUTSRQPMLLLKJIHGFEDCBA")
    cypherletter_map2.add_letters_to_mapping("LMN", "NNM")
    # map2: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
    #     'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
    #     'K': ["P"], 'L': ["M", "N"], 'M': ["L", "N"], 'N': ["L", "M"], 'O': ["L"],
    #     'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
    #     'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
    # }
    cypherletter_map3.add_letters_to_mapping("AZ", "ZA")
    # map3: Dict[str, Optional[List[str]]] = {
    #     'A': ["Z"], 'B': None, 'C': None, 'D': None, 'E': None,
    #     'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
    #     'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
    #     'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
    #     'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': ["A"],
    # }
    print(repr(cypherletter_map))
    expected1: str = "{'A': ['Z'], 'B': ['Y'], 'C': ['X'], 'D': ['W'], 'E': [" \
                     "'V'], 'F': ['U'], 'G': ['T'], 'H': ['S'], 'I': ['R'], " \
                     "'J': ['Q'], 'K': ['P'], 'L': ['O'], 'M': ['N'], " \
                     "'N': ['M'], 'O': ['L'], 'P': ['K'], 'Q': ['J'], " \
                     "'R': ['I'], 'S': ['H'], 'T': ['G'], 'U': ['F'], " \
                     "'V': ['E'], 'W': ['D'], 'X': ['C'], 'Y': ['B'], " \
                     "'Z': ['A']}"
    expected2: str = "{'A': ['Z'], 'B': ['Y'], 'C': ['X'], 'D': ['W'], 'E': [" \
                     "'V'], 'F': ['U'], 'G': ['T'], 'H': ['S'], 'I': ['R'], " \
                     "'J': ['Q'], 'K': ['P'], 'L': ['M', 'N'], 'M': ['L', " \
                     "'N'], 'N': ['L', 'M'], 'O': ['L'], 'P': ['K'], " \
                     "'Q': ['J'], 'R': ['I'], 'S': ['H'], 'T': ['G'], " \
                     "'U': ['F'], 'V': ['E'], 'W': ['D'], 'X': ['C'], " \
                     "'Y': ['B'], 'Z': ['A']}"
    expected3: str = "{'A': ['Z'], 'B': None, 'C': None, 'D': None, 'E': " \
                     "None, 'F': None, 'G': None, 'H': None, 'I': None, " \
                     "'J': None, 'K': None, 'L': None, 'M': None, 'N': None, " \
                     "'O': None, 'P': None, 'Q': None, 'R': None, 'S': None, " \
                     "'T': None, 'U': None, 'V': None, 'W': None, 'X': None, " \
                     "'Y': None, 'Z': ['A']}"
    assert repr(cypherletter_map) \
           == "CypherLetterMap({0})".format(expected1)
    assert repr(cypherletter_map2) \
           == "CypherLetterMap({0})".format(expected2)
    assert repr(cypherletter_map3) \
           == "CypherLetterMap({0})".format(expected3)


def test_eq(cypherletter_map,
            cypherletter_map2,
            cypherletter_map3,
            cypherletter_map4):
    cypherletter_map.add_letters_to_mapping("ABCD", "SELF")
    cypherletter_map2.add_letters_to_mapping("ABCDE", "OTHER")
    cypherletter_map3.add_letters_to_mapping("ABCD", "SELF")
    not_a_clm: str = "not a cypherletter map"
    assert cypherletter_map == cypherletter_map
    assert cypherletter_map == cypherletter_map3
    assert cypherletter_map != cypherletter_map2
    assert cypherletter_map != not_a_clm


def test_deepcopy(cypherletter_map):
    clm_deepcopy = copy.deepcopy(cypherletter_map)
    assert cypherletter_map.get_letter_for_cypher("A") is None
    assert clm_deepcopy.get_letter_for_cypher("A") is None
    clm_deepcopy.add_letters_to_mapping("A", "Z")
    assert cypherletter_map.get_letter_for_cypher("A") is None
    assert clm_deepcopy.get_letter_for_cypher("A") == ["Z"]

