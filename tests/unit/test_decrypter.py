#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for Decrypter in `decryptoquote` package."""
import pytest
import pyfakefs
import json

from decryptoquote.decrypter import Decrypter
from decryptoquote.cypherlettermap import CypherLetterMap
from decryptoquote.wordpatterns import WordPatterns

CORPUS_FILE_PATH = '/test.txt'
PATTERNS_FILE_PATH = '/test_patterns.json'
TEST_PATTERNS = {
        "0.1.2.3": ["THIS", "ALSO", "SOME"],
        "0.1": ["IS"],
        "0.1.2.0": ["TEXT"],
        "0.1.2.'.3": ["ISN'T"]
    }

def test_single_word(fs):
    decrypt_case(fs, "ABCD", "THIS")
    decrypt_case(fs, "AB", "IS")
    decrypt_case(fs, "ABCA", "TEXT")
    decrypt_case(fs, "ABC'D", "ISN'T")


def test_try_multiple_words(fs):
    decrypt_case(fs, "AB BCDE", "IS SOME")
    decrypt_case(fs, "ABCD EFDG DGHI", "THIS ALSO SOME")


def test_backtracking(fs):
    decrypt_case(fs, "DGHI EFDG ABCD", "SOME ALSO THIS")


def test_decrypt(fs):
    decoded_quote: str = "THIS IS SOME TEXT. THIS ISN'T."
    coded_quote: str = "ABCD CD DEFG AGHA. ABCD CDI'A."
    decrypt_case(fs, coded_quote, decoded_quote)


def setup_patterns_file(fs):
    patterns_json: str = json.dumps(TEST_PATTERNS)
    try:
        fs.create_file(PATTERNS_FILE_PATH, contents=patterns_json)
    except FileExistsError:
        with open(PATTERNS_FILE_PATH, 'w') as patterns_file:
            patterns_file.write(patterns_json)


def decrypt_case(fs, coded_quote: str, expected_decode: str):
    setup_patterns_file(fs)
    cypher_letter_map: CypherLetterMap = CypherLetterMap()
    word_patterns: WordPatterns = WordPatterns(PATTERNS_FILE_PATH)
    decrypter: Decrypter = Decrypter(
        coded_quote, cypher_letter_map, word_patterns)
    success: bool = decrypter.decrypt()
    assert success
    cypher_letter_map: CypherLetterMap = decrypter.cypher_letter_map
    assert cypher_letter_map.decode(coded_quote) == expected_decode
