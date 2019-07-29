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


class Puzzle:
    def __init__(self, input):
        self.coded_words = self.stringToCapsWords(input)
        self.decoded_words = self.initDecodedWords(self.coded_words)
        self.coding_dict = self.initCodingDict()

    def stringToCapsWords(self, input):
        input_caps = input.upper()
        return re.findall(r"[\w']+|[.,!?;]", input_caps)

    def initDecodedWords(self, input):
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

    def initCodingDict(self):
        blank_coding_dict = {}
        uppercase_list = list(string.ascii_uppercase)
        for letter in uppercase_list:
            blank_coding_dict[letter] = "*"
        return blank_coding_dict


class SearchTree:
    def __init__(self, coded_quote):
        self.total_nodes = 0
        self.current_node = Node(
            self.total_nodes,
            puzzle = Puzzle(coded_quote),
            ok_flag = "Maybe"
        )


def decryptQuote(coded_quote):
    # language_model = LanguageModel("bigtext.txt")
    search_tree = SearchTree(coded_quote_words)
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