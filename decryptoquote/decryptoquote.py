# -*- coding: utf-8 -*-

"""Main module."""

import re
import string

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

def generateBlankCodingDictionary():
    blank_coding_dict = {}
    uppercase_list = list(string.ascii_uppercase)
    for letter in uppercase_list:
        blank_coding_dict[letter] = "*"
    return blank_coding_dict

def decryptQuote(coded_quote):
    coded_quote_words = stringToCapsWords(coded_quote)
    plaintext_words = generateEmptyPlaintextWords(coded_quote_words)
    # Set up coding dictionary
    # Set up search tree to store attempted encodings
    # Loop until done:
        # Find (first) best word to check
            # lowest points, 1 point per letter, 0.5 points per undecoded letter
            # -2 points for apostrophe
        # Compare word with bigtext corpus, decode using most likely letter
        # Add decode to coding dict, decode same letter in all other words
        # Check that all fully decoded words (except last 2) match real words
            # If not, go back in tree
            # If so, add to tree
                # Also, end loop if coding dictionary is also complete
    return coded_quote
