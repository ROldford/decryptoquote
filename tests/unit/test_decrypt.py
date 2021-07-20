#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for functions in `decryptoquote` package."""
from typing import List, Dict, Optional, Tuple

import pytest
import pyfakefs

from decryptoquote import decryptoquote


# @pytest.fixture()
# def ?():

# def test_string_to_caps_words():
#     assert decryptoquote.string_to_caps_words("Svool, R'n z hgi-rmt!") \
#            == ['SVOOL', ',', "R'N", 'Z', 'HGI-RMT', '!']
#
#
# def test_get_blank_cypherletter_map():
#     assert decryptoquote.get_blank_cypherletter_map() == {
#         'A': None, 'B': None, 'C': None, 'D': None, 'E': None,
#         'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
#         'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
#         'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
#         'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': None,
#     }
#
#
# def test_add_letters_to_mapping():
#     test_map: Dict[
#         str, Optional[List[str]]] = decryptoquote.get_blank_cypherletter_map()
#     word: str = "ABCD"
#     match: str = "THIS"
#     test_map = decryptoquote.add_letters_to_mapping(test_map, word, match)
#     assert test_map == {
#         'A': ["T"], 'B': ["H"], 'C': ["I"], 'D': ["S"], 'E': None,
#         'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
#         'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
#         'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
#         'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': None,
#     }
#     match = "SOME"
#     test_map = decryptoquote.add_letters_to_mapping(test_map, word, match)
#     assert test_map == {
#         'A': ["T", "S"], 'B': ["H", "O"], 'C': ["I", "M"],
#         'D': ["S", "E"], 'E': None,
#         'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
#         'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
#         'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
#         'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': None,
#     }
#     match = "THEN"
#     test_map = decryptoquote.add_letters_to_mapping(test_map, word, match)
#     assert test_map == {
#         'A': ["T", "S"], 'B': ["H", "O"], 'C': ["I", "M", "E"],
#         'D': ["S", "E", "N"], 'E': None,
#         'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
#         'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
#         'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
#         'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': None,
#     }
#
#
# def test_add_letters_to_map_punctuation():
#     blank_map: Dict[
#         str, Optional[List[str]]] = decryptoquote.get_blank_cypherletter_map()
#     test_map: Dict[str, Optional[List[str]]] = blank_map
#     word: str = "!"
#     match: str = "!"
#     test_map = decryptoquote.add_letters_to_mapping(test_map, word, match)
#     assert test_map == blank_map
#
#
# def test_intersect_mappings():
#     # need letters where:
#     #   both maps have []
#     #   map_a has [] and map_b does not
#     #   map_b has [] and map_a does not
#     #   both have matches with no overlap
#     #   both have matches with some overlap
#     #   both have exact same matches
#     map_a: Dict[str, Optional[List[str]]] = {
#         'A': None, 'B': ["Y"], 'C': ["W", "X"], 'D': ["S", "T"],
#         'E': ["P", "Q"],
#         'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
#         'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
#         'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
#         'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': None,
#     }
#     map_b: Dict[str, Optional[List[str]]] = {
#         'A': ["Z"], 'B': None, 'C': ["U", "V"], 'D': ["R", "T"],
#         'E': ["P", "Q"],
#         'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
#         'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
#         'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
#         'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': None,
#     }
#     expected: Dict[str, Optional[List[str]]] = {
#         'A': ["Z"], 'B': ["Y"], 'C': None, 'D': ["T"], 'E': ["P", "Q"],
#         'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
#         'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
#         'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
#         'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': None,
#     }
#     assert decryptoquote.intersect_mappings(map_a, map_b) == expected
#
#
# def test_remove_solved_letters():
#     map1: Dict[str, Optional[List[str]]] = {
#         'A': ["Z"], 'B': ["Z", "Y"], 'C': ["Z", "X"], 'D': None, 'E': None,
#         'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
#         'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
#         'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
#         'U': None, 'V': None, 'W': None, 'X': None, 'Y': ["Z", "B"], 'Z': None,
#     }
#     map2: Dict[str, Optional[List[str]]] = {
#         'A': ["Z"], 'B': None, 'C': None, 'D': None, 'E': None,
#         'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
#         'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
#         'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
#         'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': None,
#     }
#     map3: Dict[str, Optional[List[str]]] = {
#         'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': None, 'E': None,
#         'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
#         'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
#         'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
#         'U': None, 'V': None, 'W': None, 'X': None, 'Y': ["B"], 'Z': None,
#     }
#     map4: Dict[str, Optional[List[str]]] = {
#         'A': ["Z"], 'B': ["Z", "Y"], 'C': ["Y", "X"], 'D': None, 'E': None,
#         'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
#         'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
#         'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
#         'U': None, 'V': None, 'W': None, 'X': None, 'Y': ["X", "B"], 'Z': None,
#     }
#     actual1: Dict[str, Optional[List[str]]] = \
#         decryptoquote.remove_solved_letters_from_map(map1)
#     actual2: Dict[str, Optional[List[str]]] = \
#         decryptoquote.remove_solved_letters_from_map(map2)
#     actual3: Dict[str, Optional[List[str]]] = \
#         decryptoquote.remove_solved_letters_from_map(map3)
#     actual4: Dict[str, Optional[List[str]]] = \
#         decryptoquote.remove_solved_letters_from_map(map4)
#     match_list1: List[Tuple[str, str]] = [("A", "Z"),
#                                           ("B", "Y"),
#                                           ("C", "X"),
#                                           ("Y", "B")]
#     match_list2: List[Tuple[str, str]] = [("A", "Z")]
#     remove_solved_letters_case(actual1, match_list1, 4)
#     remove_solved_letters_case(actual2, match_list2, 1)
#     remove_solved_letters_case(actual3, match_list1, 4)
#     remove_solved_letters_case(actual4, match_list1, 4)
#
#
# def remove_solved_letters_case(actual: Dict[str, Optional[List[str]]],
#                                expected_matches: List[Tuple[str, str]],
#                                solved_count: int) -> None:
#     for match_pair in expected_matches:
#         letter, match = match_pair
#         assert actual[letter] == [match]
#     assert len(actual["D"]) == 26 - (solved_count + 1)
#
#
# def test_remove_solved_letters_exception():
#     map1: Dict[str, Optional[List[str]]] = {
#         'A': ["Z"], 'B': ["Z"], 'C': None, 'D': None, 'E': None,
#         'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
#         'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
#         'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
#         'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': None,
#     }
#     with pytest.raises(ValueError) as except_info:
#         decryptoquote.remove_solved_letters_from_map(map1)
#     assert "A code letter was left with no possible solution" \
#            in str(except_info.value)


# def test_decrypt_with_map():
#     map1: Dict[str, Optional[List[str]]] = {
#         'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
#         'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
#         'K': ["P"], 'L': ["O"], 'M': ["N"], 'N': ["M"], 'O': ["L"],
#         'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
#         'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
#     }
#     map2: Dict[str, Optional[List[str]]] = {
#         'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
#         'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
#         'K': ["P"], 'L': ["M", "N"], 'M': ["L", "N"], 'N': ["L", "M"],
#         'O': ["L"],
#         'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
#         'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
#     }
#     map3: Dict[str, Optional[List[str]]] = {
#         'A': ["Z"], 'B': None, 'C': None, 'D': None, 'E': None,
#         'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
#         'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
#         'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
#         'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': ["A"],
#     }
#     expected1: str = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
#     expected2: str = "ZYXWVUTSRQP___LKJIHGFEDCBA"
#     expected3: str = "Z________________________A"
#     assert decryptoquote.decrypt_with_cypherletter_map(decryptoquote.LETTERS,
#                                                        map1) == expected1
#     assert decryptoquote.decrypt_with_cypherletter_map(decryptoquote.LETTERS,
#                                                        map2) == expected2


# def test_get_map_as_string():
#     map1: Dict[str, Optional[List[str]]] = {
#         'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
#         'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
#         'K': ["P"], 'L': ["O"], 'M': ["N"], 'N': ["M"], 'O': ["L"],
#         'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
#         'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
#     }
#     map2: Dict[str, Optional[List[str]]] = {
#         'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
#         'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
#         'K': ["P"], 'L': ["M", "N"], 'M': ["L", "N"], 'N': ["L", "M"], 'O': ["L"],
#         'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
#         'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
#     }
#     map3: Dict[str, Optional[List[str]]] = {
#         'A': ["Z"], 'B': None, 'C': None, 'D': None, 'E': None,
#         'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
#         'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
#         'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
#         'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': ["A"],
#     }
#     expected1: str = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
#     expected2: str = "ZYXWVUTSRQP___LKJIHGFEDCBA"
#     expected3: str = "Z________________________A"
#     assert decryptoquote.get_cypherletter_map_as_string(map1) \
#            == "Decoder:\n{0}\n{1}".format(decryptoquote.LETTERS, expected1)
#     assert decryptoquote.get_cypherletter_map_as_string(map2) \
#            == "Decoder:\n{0}\n{1}".format(decryptoquote.LETTERS, expected2)
#     assert decryptoquote.get_cypherletter_map_as_string(map3) \
#            == "Decoder:\n{0}\n{1}".format(decryptoquote.LETTERS, expected3)
