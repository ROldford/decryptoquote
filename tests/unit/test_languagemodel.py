#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for LanguageModel class in `decryptoquote` package."""

import pytest
import pyfakefs

from decryptoquote import decryptoquote

# LanguageModel takes in file path
# Init reads file at file_path, throws IOError if corpus file is invalid
# LanguageModel counts instances of each unique word using Counter instance
# TODO: enforce Singleton?
# TODO: save result as JSON, check corpus file hash on future runs and reuse?
# .isValidWord(word) checks if word exists in LanguageModel, returns bool
# .getLetterProbabilities(word):
    # word = partially decoded word, * = undecoded letter
    # returns dictionary:
        # keys are index numbers of undecoded letters
        # value is list of tuples (letter, probability)

@pytest.fixture()
def model(fs):
    test_corpus = "This is text. This is also some text. This isn't."
    corpus_file_path = '/test.txt'
    fs.create_file(corpus_file_path, contents = test_corpus)
    with open(corpus_file_path) as f:
        model = decryptoquote.LanguageModel(corpus_file_path)
    return model

def test_missing_corpus_file(fs):
    bad_file_path = '/bad.txt'
    real_file_path = '/real.txt'
    fs.create_file(real_file_path)
    with pytest.raises(IOError) as e:
        decryptoquote.LanguageModel(bad_file_path)
    assert str(e.value) == "Language model file is not valid"

def test_isValidWord(model):
    assert model.isValidWord("this") == True
    assert model.isValidWord("This") == True
    assert model.isValidWord("isn't") == True
    assert model.isValidWord("invalid") == False

def test_wordMatch(model):
    assert model.wordMatch("this", "this") == True
    assert model.wordMatch("isn't", "isn't") == True
    assert model.wordMatch("th**", "this") == True
    assert model.wordMatch("th**", "that") == True
    assert model.wordMatch("is*'*", "isn't") == True
    assert model.wordMatch("this", "that") == False
    assert model.wordMatch("th", "this") == False
    assert model.wordMatch("isnt", "isn't") == False
    assert model.wordMatch("****", "this") == True
    assert model.wordMatch("****", "that") == True

def test_getLetterProbabilities(model):
    # expect output lists to be sorted by p first,
    # then alphabetically
    assert model.getLetterProbabilities("****") == {
        0: [
            ("t", round(5/7, 3)),
            ("a", round(1/7, 3)),
            ("s", round(1/7, 3))
        ],
        1: [
            ("h", round(3/7, 3)),
            ("e", round(2/7, 3)),
            ("l", round(1/7, 3)),
            ("o", round(1/7, 3))
        ],
        2: [
            ("i", round(3/7, 3)),
            ("x", round(2/7, 3)),
            ("m", round(1/7, 3)),
            ("s", round(1/7, 3))
        ],
        3: [
            ("s", round(3/7, 3)),
            ("t", round(2/7, 3)),
            ("e", round(1/7, 3)),
            ("o", round(1/7, 3))
        ]
    }
    assert model.getLetterProbabilities("*h**") == {
        0: [("t", 1.000)],
        2: [("i", 1.000)],
        3: [("s", 1.000)]
    }
    assert model.getLetterProbabilities("***'*") == {
        0: [("i", 1.000)],
        1: [("s", 1.000)],
        2: [("n", 1.000)],
        4: [("t", 1.000)],
    }