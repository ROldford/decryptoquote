# -*- coding: utf-8 -*-

"""Main module."""

import re

def stringToCapsWords(input):
    input_caps = input.upper()
    return re.findall(r"[\w']+|[.,!?;]", input_caps)

def generateEmptyPlaintextWords(input):
    output_words = []
    for word in input:
        output_word = ""
        for char in word:
            if char.isalpha():
                output_word += "*"
            else:
                output_word += char
        output_words.append(output_word)
    return output_words

def decryptQuote(coded_quote):
    coded_quote_words = stringToCapsWords(coded_quote)
    plaintext_words = generateEmptyPlaintextWords(coded_quote_words)
    return coded_quote
