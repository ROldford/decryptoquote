#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for LanguageModel class in `decryptoquote` package."""
import json
import pytest
import pyfakefs

from decryptoquote import decryptoquote

@pytest.fixture()
def model(fs):
    test_corpus_list = ["this", "is", "text", "also", "some", "isn't"]
    test_corpus = "\n".join(test_corpus_list)
    corpus_file_path = '/test.txt'
    fs.create_file(corpus_file_path, contents=test_corpus)
    model = decryptoquote.LanguageModel(corpus_file_path)
    return model


def test_model_words(model):
    result1 = model.pattern_to_match_words("0.1.2.3")
    result2 = model.pattern_to_match_words("0.1")
    result3 = model.pattern_to_match_words("0.1.2.0")
    result4 = model.pattern_to_match_words("0.1.2.'.3")
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


def test_missing_corpus_file(fs):
    bad_file_path = '/bad.txt'
    expected_error_message: str = "Language model file not valid: {0}".format(
        bad_file_path
    )
    # real_file_path = '/real.txt'
    # fs.create_file(real_file_path)
    with pytest.raises(IOError) as e:
        decryptoquote.LanguageModel(bad_file_path)
    assert str(e.value) == expected_error_message
    # with pytest.raises(IOError) as e:
    #     decryptoquote.LanguageModel(real_file_path)
    # assert str(e.value) == expected_error_message


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
