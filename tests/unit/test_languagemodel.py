#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for WordPatterns class in `decryptoquote` package."""
import json
import os

import pytest
import pyfakefs

from decryptoquote import decryptoquote

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
def model(fs):
    patterns_json: str = json.dumps(TEST_PATTERNS)
    fs.create_file(PATTERNS_FILE_PATH, contents=patterns_json)
    model = decryptoquote.WordPatterns(PATTERNS_FILE_PATH)
    return model


# testing WordPatterns init
# - overwrite_json == True - make new json
# - json file invalid (unparseable or invalid path) - make new json
# - need to overwrite json, but corpus path invalid or None - throw error
# - otherwise - pull from json (as in fixture)


def test_init_overwrite_json(fs):
    fs.create_file(CORPUS_FILE_PATH, contents=TEST_CORPUS)
    fs.create_file(PATTERNS_FILE_PATH)
    decryptoquote.WordPatterns(PATTERNS_FILE_PATH,
                               True,
                               CORPUS_FILE_PATH)
    assert os.path.exists(PATTERNS_FILE_PATH)
    with open(PATTERNS_FILE_PATH, "r") as file:
        json_string = file.read().replace('\n', '')
        parsed_json = json.loads(json_string)
        assert parsed_json == TEST_PATTERNS


def test_init_json_file_invalid(fs):
    bad_file_path = '/bad.txt'
    fs.create_file(CORPUS_FILE_PATH, contents=TEST_CORPUS)
    decryptoquote.WordPatterns(bad_file_path,
                               corpus_file_path=CORPUS_FILE_PATH)
    with open(bad_file_path, "r") as file:
        json_string = file.read().replace('\n', '')
        parsed_json = json.loads(json_string)
        assert parsed_json == TEST_PATTERNS
    # assert 0 # TODO: stub


def test_missing_corpus_file(fs):
    bad_file_path = '/bad.txt'
    expected_error_message: str = "Language model file not valid: {0}".format(
        bad_file_path
    )
    with pytest.raises(IOError) as e:
        decryptoquote.WordPatterns(PATTERNS_FILE_PATH, True, bad_file_path)
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
    assert model.code_word_to_match_words("!") == ["!"]
