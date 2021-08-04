#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for `decryptoquote` package."""
from typing import List, Tuple

import pytest
from decryptoquote import decryptoquote


def test_string_to_caps_words():
    assert decryptoquote.string_to_caps_words("Svool, R'n z hgirmt!") == \
           ['SVOOL', ',', "R'N", 'Z', 'HGIRMT', '!']


def test_decrypt_quote():
    coded_quote: str = "OIVD DIM SMQSAM OVKD XH PMGF HXLSAM. DIMF OVKD VK " \
                       "VLMGXBV VH ZQQC VH XDH SGQLXHM."
    coded_author: str = "TVGTVGV YQGCVK"
    decoded_quote: str = "WHAT THE PEOPLE WANT IS VERY SIMPLE. THEY WANT AN " \
                         "AMERICA AS GOOD AS ITS PROMISE."
    decoded_author = "BARBARA JORDAN"

    puzzle_test_case(coded_quote, coded_author, decoded_quote, decoded_author)

    coded_quote = "Lz lv we aorbvtqr znbz we inlohqry bqr mqrr byh nbaae, "\
                  "byh tyqrvzqblyrh ge abqryzbo zeqbyye. Osjr lv znr inbly "\
                  "cnrqrge zs glyh b inloh zs lzv abqryzv."
    coded_author = "Bgqbnbw Olyisoy"
    decoded_quote = "IT IS MY PLEASURE THAT MY CHILDREN ARE FREE AND HAPPY, "\
                    "AND UNRESTRAINED BY PARENTAL TYRANNY. LOVE IS THE "\
                    "CHAIN WHEREBY TO BIND A CHILD TO ITS PARENTS."
    decoded_author = "ABRAHAM LINCOLN"

    puzzle_test_case(coded_quote, coded_author, decoded_quote, decoded_author)


def puzzle_works_check(coded_quote, decoded_quote):
    coded_words = decryptoquote.string_to_caps_words(coded_quote)
    decoded_words = decryptoquote.string_to_caps_words(decoded_quote)

    assert len(coded_words) == len(decoded_words)
    words = zip(coded_words, decoded_words)
    cypher_letter_map = decryptoquote.CypherLetterMap()
    for word_pair in words:
        coded_word, decoded_word = word_pair
        cypher_letter_map.add_word_to_mapping(coded_word, decoded_word)
    actual_decoded_quote = cypher_letter_map.decode(coded_quote.upper())
    assert actual_decoded_quote == decoded_quote.upper()


def puzzle_test_case(coded_quote, coded_author, decoded_quote, decoded_author):
    puzzle_works_check(coded_quote, decoded_quote)
    author_result: str = decryptoquote.decrypt_quote(
        coded_quote,
        coded_author,
        rebuild_patterns=True)
    no_author_result: str = decryptoquote.decrypt_quote(
        coded_quote,
        rebuild_patterns=True)
    # author_result_with_cypher: str = decryptoquote.decrypt_quote(
    #     coded_quote,
    #     show_cypher=True,
    #     rebuild_patterns=True)
    # print(author_result_with_cypher)
    # print(author_result)
    assert no_author_result == decoded_quote
    actual_author = author_result.split("\n")[1]
    for letter_pair in zip(decoded_author, actual_author):
        expected_letter, actual_letter = letter_pair
        assert (expected_letter == actual_letter or actual_letter == '_')
