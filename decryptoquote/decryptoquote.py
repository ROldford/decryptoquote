# -*- coding: utf-8 -*-

"""Main module."""

import re
import string
from collections import Counter

from anytree import Node

class LanguageModel:
    def __init__(self, file_path):
        corpus_text = ""
        try:
            with open(file_path) as file:
                corpus_text = file.read()
        except IOError as ioerr:
            raise IOError("Language model file is not valid") from ioerr
        word_list = re.findall("[a-z']+", corpus_text.lower())
        self.WORD_COUNTER = Counter(word_list)
        self.TOTAL_WORDS = sum(self.WORD_COUNTER.values())

    def wordMatch(self, word, elem):
        word_length = len(word)
        elem_length = len(elem)
        if word_length != elem_length:
            return False
        for i in range(word_length):
            if word[i] != "*" and word[i] != elem[i]:
                return False
        return True

    def isValidWord(self, word):
        return word.lower() in self.WORD_COUNTER

    def getLetterProbabilities(self, word):
        return_dict = {}
        filtered_word_dict = {
            k: v for k, v in self.WORD_COUNTER.items() if self.wordMatch(word, k)
        }
        filtered_word_counter = Counter(filtered_word_dict)
        filtered_total_words = sum(filtered_word_counter.values())
        for i in range(len(word)):
            # TODO: replace literal with imported constant
            if word[i] == "*":
                current_char_counter = Counter()
                for filtered_word, count in filtered_word_counter.items():
                    filtered_char = filtered_word[i]
                    current_char_counter += Counter({filtered_char: count})
                current_char_count_list = list(current_char_counter.items())
                current_char_total = sum(current_char_counter.values())
                current_char_count_list = [
                    (
                        i[0], round(i[1]/current_char_total, 3)
                    ) for i in current_char_count_list
                ]
                # Sort aphabetically, then by probability
                # sorted is stable sort,
                # so list is sorted by p, then alphabetically
                current_char_count_list = sorted(current_char_count_list)
                current_char_count_list = sorted(
                    current_char_count_list,
                    key=lambda element: element[1],
                    reverse=True)
                return_dict.update({i: current_char_count_list})
        return return_dict





def stringToCapsWords(input):
    input_caps = input.upper()
    return re.findall(r"[\w']+|[.,!?;]", input_caps)

def generateEmptyPlaintextWords(input):
    output_words = []
    for word in input:
        output_word = ""
        for char in word:
            if char.isalpha():
                # TODO: replace literal with imported constant
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

def generateSearchTree(coded_quote_words):
    # Set up search tree to store attempted encodings
        # Each node has current coding_dict, plaintext_words, OK flag
    blank_plaintext_words = generateEmptyPlaintextWords(coded_quote_words)
    blank_coding_dict = generateBlankCodingDictionary()
    return Node(
        "0",
        coding_dict = blank_coding_dict,
        plaintext_words = blank_plaintext_words,
        ok_flag = "Maybe"
        # TODO: Make this into imported constant
        )

# generation of new search tree nodes involves checking number of nodes
# can just use iteration to get all nodes and use .length
# may need to switch to generator class with running total
# in that case, generate_search_tree will be class method
# can have this function call class method to keep unit tests solid



def decryptQuote(coded_quote):
    coded_quote_words = stringToCapsWords(coded_quote)
    search_tree_root = generateSearchTree(coded_quote_words)
    # Loop until done:
        # Check validity of current node's decoding dict
            # Valid if >95% of all fully decoded words (except last 2)...
            # ...match words in bigtext corpus
            # If not valid, set OK flag to "NO" and go to parent
            # If so, and coding dict is not complete, continue
            # If so, and coding dict is complete, you're done!
        # Generate children if none present
            # Find all lowest score words to check
                # 1 point per letter, 0.5 points per undecoded letter
                # -2 points for apostrophe
            # For each lowest score word:
                # For each undecoded letter:
                    # Compare word with bigtext corpus
                    # Generate children for decodings of letter (>20% chance)
                        # OK flag = "Maybe"
                        # Update coding_dict
                        # Use dict to update plaintext_words
        # If no children can be generated, set OK to "No" and go to parent
        # Drop down to next child with OK = "Maybe"
            # If no available children, set OK to "No" and go to parent
    return coded_quote
