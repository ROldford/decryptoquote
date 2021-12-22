#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for WordPatterns class in `decryptoquote` package."""
import json
import os

import pytest
import pyfakefs
import mongomock

from decryptoquote.wordpatterns import WordPatterns

CORPUS_FILE_PATH = '/test.txt'
PATTERNS_FILE_PATH = '/test_patterns.json'
TEST_PATTERNS = {
        "0.1.2.3": ["THIS", "ALSO", "SOME"],
        "0.1": ["IS"],
        "0.1.2.0": ["TEXT"],
        "0.1.2.'.3": ["ISN'T"]
    }
TEST_CORPUS_LIST = ["this", "is", "text", "also", "some", "isn't"]
TEST_CORPUS = "\n".join(TEST_CORPUS_LIST)


@pytest.fixture()
def collection() -> mongomock.Collection:
    collection: mongomock.Collection = mongomock.MongoClient().db.collection
    documents = []
    for pattern, words in TEST_PATTERNS.items():
        for word in words:
            documents.append({WordPatterns.WORD_KEY: word,
                              WordPatterns.PATTERN_KEY: pattern})
    collection.insert_many(documents)
    return collection

@pytest.fixture()
def model(collection) -> WordPatterns:

    # patterns_json: str = json.dumps(TEST_PATTERNS)
    # fs.create_file(PATTERNS_FILE_PATH, contents=patterns_json)
    # model = WordPatterns(PATTERNS_FILE_PATH)
    model = WordPatterns(collection)
    return model


# testing WordPatterns init
# - overwrite_json == True - make new json
# - json file invalid (unparseable or invalid path) - make new json
# - need to overwrite json, but corpus path invalid or None - throw error
# - otherwise - pull from json (as in fixture)


def test_init_overwrite_patterns(fs, collection):
    # smoke test: see if this works without exception thrown
    fs.create_file(CORPUS_FILE_PATH, contents=TEST_CORPUS)
    WordPatterns(collection,
                 True,
                 CORPUS_FILE_PATH)


def test_missing_corpus_file(fs, collection):
    bad_file_path = '/bad.txt'
    with pytest.raises(OSError) as e:
        WordPatterns(collection, True, bad_file_path)
    assert "No such file" in str(e.value)
    expected_error_message: str = "No valid language file given"
    with pytest.raises(ValueError) as e:
        WordPatterns(collection, True)
    assert str(e.value) == expected_error_message


def test_model_words(model):
    result1 = model.pattern_to_match_words("0.1.2.3")
    result2 = model.pattern_to_match_words("0.1")
    result3 = model.pattern_to_match_words("0.1.2.0")
    result4 = model.pattern_to_match_words("0.1.2.'.3")
    result5 = model.pattern_to_match_words("!")
    assert len(result1) == 3
    assert "THIS" in result1
    assert "ALSO" in result1
    assert "SOME" in result1
    assert len(result2) == 1
    assert result2 == ["IS"]
    assert len(result3) == 1
    assert result3 == ["TEXT"]
    assert len(result4) == 1
    assert result4 == ["ISN'T"]
    assert result5 == ["!"]


def test_word_to_pattern(model):
    assert model.word_to_pattern("this") == "0.1.2.3"
    assert model.word_to_pattern("text") == "0.1.2.0"
    assert model.word_to_pattern("isn't") == "0.1.2.'.3"
    assert model.word_to_pattern("long-term") == "0.1.2.3.-.4.5.6.7"


def test_code_word_to_match_words(model):
    assert model.code_word_to_match_words("ABCA") == ["TEXT"]
    result2 = model.code_word_to_match_words("ABCD")
    assert "THIS" in result2
    assert "ALSO" in result2
    assert "SOME" in result2
    assert model.code_word_to_match_words("AB") == ["IS"]
    assert model.code_word_to_match_words("ABC'D") == ["ISN'T"]
    assert model.code_word_to_match_words("ABC") == []
    assert model.code_word_to_match_words("!") == ["!"]
    assert model.code_word_to_match_words(".") == ["."]


def test_add_new_words(model):
    new_words = ["NEW", "words"]
    for new_word in new_words:
        assert model.code_word_to_match_words(new_word) == []
    model.add_new_words(new_words)
    for new_word in new_words:
        assert new_word.upper() in model.code_word_to_match_words(new_word)


def test_save_corpus_from_patterns(model):
    assert True
