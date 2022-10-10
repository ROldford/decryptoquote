#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for `decryptoquote` package."""
from typing import List, Dict

import pytest
import mongomock

from decryptoquote.cypherlettermap import CypherLetterMap
from decryptoquote.helpers import string_to_caps_words
from decryptoquote.decryptoquote import (decrypt_quote_fully,
                                         MONGO_HOST)


def test_string_to_caps_words():
    assert string_to_caps_words("Svool, R'n z hgirmt!") == \
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
    coded_words = string_to_caps_words(coded_quote)
    decoded_words = string_to_caps_words(decoded_quote)

    assert len(coded_words) == len(decoded_words)
    words = zip(coded_words, decoded_words)
    cypher_letter_map = CypherLetterMap()
    for word_pair in words:
        coded_word, decoded_word = word_pair
        cypher_letter_map.add_word_to_mapping(coded_word, decoded_word)
    actual_decoded_quote = cypher_letter_map.decode(coded_quote.upper())
    assert actual_decoded_quote == decoded_quote.upper()


@mongomock.patch(servers=((MONGO_HOST),))
def puzzle_test_case(coded_quote, coded_author, decoded_quote, decoded_author):
    puzzle_works_check(coded_quote, decoded_quote)
    author_results: List[Dict[str, str]] = decrypt_quote_fully(
        coded_quote,
        coded_author,
        rebuild_patterns=True)
    no_author_results: List[Dict[str, str]] = decrypt_quote_fully(
        coded_quote,
        rebuild_patterns=True)
    no_author_quotes = [x.get('decoded_quote') for x in no_author_results]
    assert decoded_quote in no_author_quotes
    for result in author_results:
        actual_quote = result.get('decoded_quote')
        actual_author = result.get('decoded_author')
        if actual_quote == decoded_quote and actual_author is not None:
            for letter_pair in zip(decoded_author, actual_author):
                expected_letter, actual_letter = letter_pair
                assert (
                    expected_letter == actual_letter or actual_letter == "_")
