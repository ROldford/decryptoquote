#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for LanguageModel class in `decryptoquote` package."""

import pytest
import pyfakefs

from decryptoquote import decryptoquote

@pytest.fixture()
def model(fs):
    test_corpus = "This is text. This is also some text. This isn't."
    corpus_file_path = '/test.txt'
    fs.create_file(corpus_file_path, contents=test_corpus)
    with open(corpus_file_path) as f:
        model = decryptoquote.LanguageModel(corpus_file_path)
    return model


def test_model_words(model):
    assert list(model.WORD_COUNTER.items()) == [
        ('THIS', 3), ('IS', 2), ('TEXT', 2),
        ('ALSO', 1), ('SOME', 1), ("ISN'T", 1)
    ]


def test_missing_corpus_file(fs):
    bad_file_path = '/bad.txt'
    real_file_path = '/real.txt'
    fs.create_file(real_file_path)
    with pytest.raises(IOError) as e:
        decryptoquote.LanguageModel(bad_file_path)
    assert str(e.value) == "Language model file is not valid"


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

