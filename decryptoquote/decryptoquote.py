# -*- coding: utf-8 -*-

"""Main module."""

import re
import string
from collections import Counter
from typing import Dict, List, Tuple, Optional

from anytree import Node


class LanguageModel:
    def __init__(self, file_path: str) -> None:
        """
        Create LanguageModel instance
        :param file_path: path to language corpus file
        """
        try:
            with open(file_path) as file:
                corpus_text: str = file.read()
        except IOError as ioerr:
            raise IOError("Language model file is not valid") from ioerr
        word_list = self.word_lister(corpus_text)
        self.WORD_COUNTER = Counter(word_list)
        self.TOTAL_WORDS = sum(self.WORD_COUNTER.values())

    @staticmethod
    def word_lister(corpus: str) -> List[str]:
        """
        Converts corpus into list of words (no punct. except apostrophe)
        :param corpus: large sample of English language
        :return: list of words in corpus

        >>> LanguageModel.word_lister("This is also some text. This isn't.")
        ['this', 'is', 'also', 'some', 'text', 'this', "isn't"]
        >>> LanguageModel.word_lister("")
        []
        >>> LanguageModel.word_lister(".,:;")
        []
        """
        return re.findall("[a-z']+", corpus.lower())

    @staticmethod
    def word_match(word: str, elem: str) -> bool:
        """
        Check if word pattern from puzzle matches word from corpus
        :param word: word pattern from puzzle (* = unknown letter)
        :param elem: word from corpus
        :return: match status

        >>> LanguageModel.word_match("", "")
        True
        >>> LanguageModel.word_match("***", "this")
        False
        >>> LanguageModel.word_match("****", "this")
        True
        >>> LanguageModel.word_match("****", "word")
        True
        >>> LanguageModel.word_match("th**", "this")
        True
        >>> LanguageModel.word_match("th**", "that")
        True
        >>> LanguageModel.word_match("th**", "word")
        False
        """
        word_length = len(word)
        elem_length = len(elem)
        if word_length != elem_length:
            return False
        for i in range(word_length):
            if word[i] != "*" and word[i] != elem[i]:
                return False
        return True

    def is_valid_word(self, word: str) -> bool:
        """
        Check if given word exists in the language model
        :param word: word to check
        :return: whether word is valid (in language model)
        """
        return word.lower() in self.WORD_COUNTER

    def get_possible_word_matches(self, pattern: str) -> List[Tuple[str, ...]]:
        """
        Given coded word pattern, produce possible char matches
        :param pattern: coded word pattern (* = undecoded)
        :return: list of possible char matches (as tuples)

        Example:
            given "***'*",
                produces [('I', 'S', 'N', 'T'), ('D', 'O', 'N', 'T'), ...]
            given "HO*S*",
                produces [('U', 'E'), ...]
        """
        # determine indices of wildcards in pattern, store in tuple
        # find matching words
        # for each matching word:
        #   Extract letters at wildcard indices
        #   Convert to uppercase
        #   Make tuple
        #   Append to list


    # def get_letter_probabilities(self, word: str) -> \
    #         Dict[int, List[Tuple[str, float]]]:
    #     """
    #     Produces letter probabilities for unknown letters in given word pattern
    #     :param word: word pattern from puzzle
    #     :return: letter probabilities dictionary
    #         key: index of unknown letter in word pattern
    #         value: sorted list of (letter, probability) tuples
    #                (highest p first, alpha on ties)
    #     """
    #     return_dict = {}
    #     matching_word_dict = {
    #         k: v for k, v in self.WORD_COUNTER.items() if self.word_match(
    #             word, k
    #         )
    #     }
    #     matching_word_counter = Counter(matching_word_dict)
    #     # matching_total_words = sum(matching_word_counter.values())
    #     for i in range(len(word)):
    #         # TODO: replace literal with imported constant
    #         if word[i] == "*":
    #             current_char_counter = Counter()
    #             # go through each wildcard, find possible matches,
    #             # add to Counter
    #             for matching_word, count in matching_word_counter.items():
    #                 matching_char = matching_word[i]
    #                 current_char_counter += Counter({matching_char: count})
    #             current_char_count_list = list(current_char_counter.items())
    #             current_char_total = sum(current_char_counter.values())
    #             current_char_count_list = [
    #                 (
    #                     char_match[0],
    #                     round(char_match[1]/current_char_total, 3)
    #                 ) for char_match in current_char_count_list
    #             ]
    #             # Sort alphabetically, then by probability
    #             # sorted is stable sort,
    #             # so sorting alphabetically first, then by probability
    #             # produces list is sorted by p, then alphabetically
    #             current_char_count_list = self.sort_char_counts(
    #                 current_char_count_list
    #             )
    #             return_dict.update({i: current_char_count_list})
    #     return return_dict
    #
    # @staticmethod
    # def sort_char_counts(char_count_list: List[Tuple[str, float]]) ->\
    #         List[Tuple[str, float]]:
    #     """
    #     Sorts char count list by probability, then alphabetically on ties
    #     :param char_count_list: list of character count tuples
    #     :return: sorted list
    #
    #     >>> LanguageModel.sort_char_counts(
    #     ...     [('s', 0.1), ('t', 0.5), ('e', 0.1)]
    #     ... )
    #     [('t', 0.5), ('e', 0.1), ('s', 0.1)]
    #     """
    #     char_count_list = sorted(char_count_list)
    #     char_count_list = sorted(
    #         char_count_list,
    #         key=lambda element: element[1],
    #         reverse=True)
    #     return char_count_list





class Puzzle:
    """
    Data type for cryptoquote puzzle
    :param coding_dict: dict of coded letters and matching decoded letters
    :param coded_quote_words: list of original words in cryptoquote
    :param decoded_quote_words: list of words being decoded (* = unknown letter)
    :param coded_author_words: list of words in author part of cryptoquote
    :param decoded_author_words: list of author part words being decoded
    """
    def __init__(self,
                 coding_dict: Dict[str, str],
                 coded_quote_words: List[str],
                 decoded_quote_words: List[str],
                 coded_author_words: Optional[List[str]] = None,
                 decoded_author_words: Optional[List[str]] = None
                 ) -> None:
        # TODO: remove isinstance use (but what can replace it?)
        self.coding_dict = coding_dict
        self.coded_quote_words = coded_quote_words
        self.decoded_quote_words = decoded_quote_words
        self.coded_author_words = coded_author_words
        self.decoded_author_words = decoded_author_words


class PuzzleFactory:
    def make_inital_puzzle(self,
                           coded_quote: str,
                           coded_author: str = None) -> Puzzle:
        coded_quote_words = self.string_to_caps_words(coded_quote)
        decoded_quote_words = self.init_decoded_words(coded_quote_words)
        coding_dict = self.init_coding_dict()
        if coded_author is not None:
            coded_author_words = self.string_to_caps_words(
                coded_author
            )
            decoded_author_words = self.init_decoded_words(coded_author_words)
            puzzle = Puzzle(coding_dict, coded_quote_words, decoded_quote_words,
                            coded_author_words, decoded_author_words)
            return puzzle
        else:
            puzzle = Puzzle(coding_dict, coded_quote_words, decoded_quote_words)
            return puzzle

    def string_to_caps_words(self, in_string: str) -> List[str]:
        """
        Convert string to list of words in caps
        :param in_string: input string
        :return: word list (all caps)

        >>> self.string_to_caps_words("Svool, R'n z hgirmt!")
        ['SVOOL', ',', "R'N", 'Z', 'HGIRMT', '!']
        """
        return re.findall(r"[\w']+|[.,!?;]", in_string.upper())

    def init_decoded_words(self, in_words: List[str]) -> List[str]:
        """
        Given coded words list, produce initial decoded words list
            (all words and punctuation copied, but with letter placeholders)
        :param in_words: coded words list
        :return: decoded words list (with letter placeholders)

        >>> self.init_decoded_words(
        ...     ['SVOOL', ',', "R'N", 'Z', 'HGIRMT', '!']
        ... )
        ['*****', ',', "*'*", '*', '******', '!']
        """
        output_words = []
        for word in in_words:
            output_word = ""
            for char in word:
                if char.isalpha():
                    # TODO: replace literal with imported constant
                    output_word += "*"
                else:
                    output_word += char
            output_words.append(output_word)
        return output_words

    def init_coding_dict(self) -> Dict[str, str]:
        """
        Produce blank coding dictionary
            keys: capital letters
            values: * placeholder
        :return: blank coding dictionary

        >>> PuzzleFactory.init_coding_dict() #doctest: +ELLIPSIS
        {'A': '*', 'B': '*', 'C': '*', ... 'Z': '*'}
        """
        blank_coding_dict = {}
        uppercase_list = list(string.ascii_uppercase)
        for letter in uppercase_list:
            blank_coding_dict[letter] = "*"
        return blank_coding_dict


# class SearchTree:
#     '''
#
#     '''
#     def __init__(self, coded_quote: str) -> None:
#         self.__nodes = []
#         self.__current_node_index = 0
#         self.__nodes.append(
#             Node(
#                 self.__current_node_index,
#                 puzzle = Puzzle(coded_quote),
#                 ok_flag = "Maybe"
#             )
#         )
#
#     def getCurrentNode(self):
#         return self.__nodes[self.__current_node_index]


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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
