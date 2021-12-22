#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for Decrypter in `decryptoquote` package."""
import pytest
import pyfakefs
import mongomock
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

def generate_collection(test_patterns: Dict[str, List[str]]) -> mongomock.Collection:
    collection: mongomock.Collection = mongomock.MongoClient().db.collection
    documents = []
    for pattern, words in test_patterns.items():
        for word in words:
            documents.append({WordPatterns.WORD_KEY: word,
                              WordPatterns.PATTERN_KEY: pattern})
    collection.insert_many(documents)
    return collection


@pytest.fixture()
def collection() -> mongomock.Collection:
    return generate_collection(TEST_PATTERNS)


@pytest.fixture()
def collection2() -> mongomock.Collection:
    new_test_patterns: Dict[str, List[str]] = {
        k: TEST_PATTERNS[k] for k in TEST_PATTERNS.keys()}
    new_test_patterns["0.1.2.0"].append("TENT")
    return generate_collection(new_test_patterns)


def test_single_word(collection):
    decrypt_case(collection, "ABCD", "THIS")
    decrypt_case(collection, "AB", "IS")
    decrypt_case(collection, "ABCA", "TEXT")
    decrypt_case(collection, "ABC'D", "ISN'T")


def test_try_multiple_words(collection):
    decrypt_case(collection, "AB BCDE", "IS SOME")
    decrypt_case(collection, "ABCD EFDG DGHI", "THIS ALSO SOME")


def test_backtracking(collection):
    decrypt_case(collection, "DGHI EFDG ABCD", "SOME ALSO THIS")


def test_decrypt(collection):
    decoded_quote: str = "THIS IS SOME TEXT. THIS ISN'T."
    coded_quote: str = "ABCD CD DEFG AGHA. ABCD CDI'A."
    decrypt_case(collection, coded_quote, decoded_quote)


def setup_patterns_file(fs):
    patterns_json: str = json.dumps(TEST_PATTERNS)
    try:
        fs.create_file(PATTERNS_FILE_PATH, contents=patterns_json)
    except FileExistsError:
        with open(PATTERNS_FILE_PATH, 'w') as patterns_file:
            patterns_file.write(patterns_json)


def decrypt_case(collection, coded_quote: str, expected_decode: str):
    decrypter: Decrypter = build_decrypter(collection, coded_quote)
    success: bool = decrypter.decrypt()
    assert success
    cypher_letter_map: CypherLetterMap = decrypter.cypher_letter_map
    assert cypher_letter_map.decode(coded_quote) == expected_decode


def build_decrypter(collection, coded_quote: str) -> Decrypter:
    cypher_letter_map: CypherLetterMap = CypherLetterMap()
    word_patterns: WordPatterns = WordPatterns(collection)
    decrypter: Decrypter = Decrypter(
        coded_quote, cypher_letter_map, word_patterns)
    return decrypter
