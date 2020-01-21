#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for LanguageModel class in `decryptoquote` package."""
import json
import pytest
import pyfakefs

from decryptoquote import decryptoquote

@pytest.fixture()
def model(fs):
    test_corpus_dict = {
        "this": 1,
        "is": 1,
        "text": 1,
        "also": 1,
        "some": 1,
        "isn't": 1
    }
    test_corpus_json = json.dumps(test_corpus_dict)
    corpus_file_path = '/test.txt'
    fs.create_file(corpus_file_path, contents=test_corpus_json)
    model = decryptoquote.LanguageModel(corpus_file_path)
    return model


def test_model_words(model):
    assert list(model.CORPUS) == [
        "this", "is", "text", "also", "some", "isn't"
    ]


def test_missing_corpus_file(fs):
    expected_error_message: str = "Language model file is not valid"
    bad_file_path = '/bad.txt'
    real_file_path = '/real.txt'
    fs.create_file(real_file_path)
    with pytest.raises(IOError) as e:
        decryptoquote.LanguageModel(bad_file_path)
    assert str(e.value) == expected_error_message
    with pytest.raises(IOError) as e:
        decryptoquote.LanguageModel(real_file_path)
    assert str(e.value) == expected_error_message


def test_is_valid_word(model):
    assert model.is_valid_word("this") is True
    assert model.is_valid_word("This") is True
    assert model.is_valid_word("isn't") is True
    assert model.is_valid_word("invalid") is False


def test_get_possible_word_matches(model):
    assert model.get_possible_word_matches("***'*") == [
        ['I', 'S', 'N', 'T']
    ]
    assert model.get_possible_word_matches("T***") == [
        ['H', 'I', 'S'],
        ['E', 'X', 'T']
    ]
    assert model.get_possible_word_matches("A*") == []
    assert model.get_possible_word_matches("i*") == [
        ['S']
    ]


def test_get_matching_words(model):
    assert model.get_matching_words("T***") == ["THIS", "TEXT"]
    assert model.get_matching_words("i*") == ["IS"]
    assert model.get_matching_words("***'*") == ["ISN'T"]

