# -*- coding: utf-8 -*-

"""Main module."""
import copy
import json
import os
import pprint
import re
import string
from typing import Dict, List, Optional, Union, Tuple

UNKNOWN: str = "*"
PATTERNS_JSON: str = "word_patterns.json"
CORPUS_FILE: str = "words_alpha_apos.txt"
# SHORT_WORDS_CORPUS_FILE: str = "words_small.txt"
IN_WORD_PUNCT: str = "'-"
NON_WORD_PUNCT: str = ".,!?;"
PUNCTUATION: str = "{0}{1}".format(IN_WORD_PUNCT, NON_WORD_PUNCT)
LETTERS: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
EXCEPT_MESSAGE: str = "A code letter was left with no possible solution"


class WordPatterns:
    def __init__(self,
                 pattern_dict_file_path: str,
                 overwrite_json: bool = False,
                 corpus_file_path: str = None) -> None:
        """
        Create WordPatterns instance from given corpus file
            corpus file is large file of English text, .txt format
        :param corpus_file_path: path to language corpus file
        :exception IOError if corpus file is invalid
        """
        # TODO: enforce Singleton?
        if overwrite_json or not os.path.exists(pattern_dict_file_path):
            # we need a new patterns JSON, so get words from corpus text file
            self._patterns: Dict[str, List[str]] = {}
            try:
                with open(corpus_file_path, 'r') as file:
                    # TODO: store as tree
                    word_list: List[str] = [
                        s.upper() for s in file.read().splitlines()
                    ]
                    for word in word_list:
                        pattern: str = self.word_to_pattern(word)
                        if pattern not in self._patterns:
                            self._patterns[pattern] = [word]
                        else:
                            self._patterns[pattern].append(word)
            except Exception as err:
                raise IOError(
                    f"Language model file not valid: {corpus_file_path}"
                ) from err
            try:
                with open(pattern_dict_file_path, "w") as file:
                    json.dump(self._patterns, file)
            except Exception as err:
                raise IOError(
                    f"Patterns file not created correctly: {pattern_dict_file_path}"
                ) from err
        else:
            # just load patterns JSON
            with open(pattern_dict_file_path, "r") as file:
                self._patterns = json.load(file)

    @staticmethod
    def word_to_pattern(word: str) -> str:
        """

        :param word:
        :return:
        """
        word = word.upper()
        pattern_num = 0
        letter_nums: Dict[str, str] = {}
        word_pattern = []
        for letter in word:
            if letter not in PUNCTUATION:
                if letter not in letter_nums:
                    letter_nums[letter] = str(pattern_num)
                    pattern_num += 1
                word_pattern.append(letter_nums[letter])
            else:
                word_pattern.append(letter)
        return ".".join(word_pattern)

    def pattern_to_match_words(self, pattern: str) -> List[str]:
        if pattern not in self._patterns:
            return [pattern]
        else:
            return self._patterns[pattern]

    def code_word_to_match_words(self, code_word: str) -> List[str]:
        pattern: str = self.word_to_pattern(code_word)
        return self.pattern_to_match_words(pattern)

    def add_words_to_saved_patterns(self, words: List[str]):
        pass  # TODO: stub

    def make_corpus_from_patterns(self, corpus_file_path: str) -> None:
        pass  # TODO: stub


class WordTreeNode:
    def __init__(self):
        self._children: Dict[str, WordTreeNode] = {}
        self._word_end: bool = False

    def add_word(self, word: str) -> None:
        if len(word) == 0:
            self._word_end = True
        else:
            word_first: str = word.upper()[0]
            word_rest: str = word.upper()[1:]
            if word[0] in self._children:
                child: WordTreeNode = self._children[word_first]
                child.add_word(word_rest)
            else:
                child: WordTreeNode = WordTreeNode()
                self._children[word_first] = child
                child.add_word(word_rest)

    def is_word(self, word: str) -> bool:
        if len(word) == 0:
            return self._word_end
        else:
            word_first: str = word.upper()[0]
            word_rest: str = word.upper()[1:]
            if word_first in self._children:
                child: WordTreeNode = self._children[word_first]
                return child.is_word(word_rest)
            else:
                return False

    def find_words(self, word: str) -> List[str]:
        return self._find_words(word, [])

    def _find_words(self, word: str, acc: List[str]) -> List[str]:
        if len(word) == 0:
            if not self._word_end:  # invalid word
                return []
            else:
                return acc
        else:
            word_first: str = word.upper()[0]
            word_rest: str = word.upper()[1:]
            if word_first == "_":
                # for each child letter,
                # append child letter to copy of acc
                # self.find_words(word_rest, acc copy)
                # merge resulting lists together and return
                return_value: List[str] = []
                for key, value in self._children.items():
                    new_acc = []
                    if len(acc) > 0:
                        new_acc.append(acc[0] + key)
                    else:
                        new_acc.append(key)
                    # return_value.extend(self._find_words(word_rest, new_acc))
                    rec_result = value._find_words(word_rest, new_acc)
                    return_value = return_value + rec_result
                return return_value
            elif word_first in self._children.keys():
                # append word_first to end of acc
                # return self.find_words(word_rest, acc
                new_acc = []
                if len(acc) > 0:
                    new_acc.append(acc[0] + word_first)
                else:
                    new_acc.append(word_first)
                child: WordTreeNode = self._children[word_first]
                return child._find_words(word_rest, new_acc)
            else:
                return []


class CypherLetterMap:
    # TODO: develop this
    def __init__(self):
        self._clmap: Dict[str, Optional[List[str]]] = {}
        for letter in LETTERS:
            self._clmap[letter] = None

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self._clmap!r})')

    def __str__(self):
        key: List[str] = []
        for letter in LETTERS:
            if self._clmap[letter] is None \
                    or len(self._clmap[letter]) != 1:
                key.append("_")
            else:
                key.append(self._clmap[letter][0])
        return "Decoder:\n{0}\n{1}".format(LETTERS, "".join(key))

    def get_letter_for_cypher(self, cypher: str) -> Optional[List[str]]:
        return self._clmap[cypher]

    def decrypt(self, code: str) -> str:
        code = code.upper()
        decoded: List[str] = list(copy.deepcopy(code))
        for i in range(len(code)):
            letter: str = code[i]
            if letter in LETTERS:  # is it an A-Z letter?
                match: Optional[List[str]] = \
                    self.get_letter_for_cypher(letter)
                if match is not None and len(match) == 1:
                    decoded[i] = match[0]
                else:
                    decoded[i] = "_"
        return "".join(decoded)

    def add_letters_to_mapping(self,
                               word: str,
                               match: str) -> None:
        for i in range(len(word)):
            if match[i] not in PUNCTUATION:
                if self._clmap[word[i]] is None:
                    self._clmap[word[i]] = [match[i]]
                elif match[i] not in self._clmap[word[i]]:
                    self._clmap[word[i]].append(match[i])

    def intersect_mappings(self,
                           other: 'CypherLetterMap') -> None:
        for letter in LETTERS:
            if self._clmap[letter] is None:
                self._clmap[letter] = copy.deepcopy(
                    other.get_letter_for_cypher(letter))
            elif other.get_letter_for_cypher(letter) is not None:
                intersection: List[str] = []
                for mapped_letter in self._clmap[letter]:
                    if mapped_letter in other.get_letter_for_cypher(letter):
                        if mapped_letter not in intersection:
                            intersection.append(mapped_letter)
                if not intersection:
                    raise ValueError(EXCEPT_MESSAGE)
                else:
                    self._clmap[letter] = intersection

    def remove_solved_letters_from_map(self) -> None:
        done: bool = False
        while not done:
            done = True  # assume done

            # scan through map and track solved letters
            solved_letters = []
            for letter in LETTERS:
                if self._clmap[letter] is not None \
                        and len(self._clmap[letter]) == 1:
                    if self._clmap[letter][0] in solved_letters:
                        # 2 code letters with same letter mapping = no solution
                        raise ValueError(EXCEPT_MESSAGE)
                    else:
                        solved_letters.append(self._clmap[letter][0])

            # removed solved letters as possibilities for other letters
            for letter in LETTERS:
                for solved in solved_letters:
                    if self._clmap[letter] is not None:
                        if len(self._clmap[letter]) != 1 \
                                and (solved in self._clmap[letter]):
                            self._clmap[letter].remove(solved)
                            if len(self._clmap[letter]) == 1:
                                # new letter is now solved,
                                # so we're not done yet!
                                done = False
                            elif len(self._clmap[letter]) == 0:
                                raise ValueError(EXCEPT_MESSAGE)
                        elif len(self._clmap[letter]) == 0:
                            raise ValueError(EXCEPT_MESSAGE)
                    else:
                        # replace with all letters,
                        # then remove this letter and solved letter
                        self._clmap[letter] = [
                            char for char in LETTERS if char not in [letter,
                                                                     solved]]
    #
    # def get_cypherletter_map_as_string(
    #     cypherletter_map: Dict[str, List[str]]) -> str:
    #     key: List[str] = []
    #     for letter in LETTERS:
    #         if cypherletter_map[letter] is None \
    #             or len(cypherletter_map[letter]) != 1:
    #             key.append("_")
    #         else:
    #             key.append(cypherletter_map[letter][0])
    #     return "Decoder:\n{0}\n{1}".format(LETTERS, "".join(key))


class SolutionTreeNode:
    def __init__(self,
                 coded_quote: str,
                 cypherletter_map: CypherLetterMap,
                 wordtree: WordTreeNode = None):
        self._coded_quote: str = coded_quote
        self._cypherletter_map: CypherLetterMap = cypherletter_map
        if wordtree is None:
            self._wordtree = WordTreeNode
        self._wordtree: WordTreeNode = wordtree
        self._children: List[SolutionTreeNode] = []

    def generate_solutions(self) -> List[Tuple[str, Dict[str, List[str]]]]:
        # choose first incomplete word from decoded quote
        # get all possible word matches using WordTreeNode
        # for each match, update coding dictionary with new matches from word
        #   for each matching letter
        #       check that new matching letter is in coding dict possibilities
        #       if not, return []
        #       if so, remove all other letters
        #       update other letters using remove_solved_letters
        #       return [] if remove_solved_letters fails
        #   create child node and run generate_solutions on it
        decoded_list: List[str] = string_to_caps_words(self._decoded_quote)
        coded_list: List[str] = string_to_caps_words(self._coded_quote)
        incomplete_word: Tuple[str, str] = self._get_first_incomplete_word(
            coded_list, decoded_list)
        word_coded: str = incomplete_word[0]
        word_decoded: str = incomplete_word[1]
        possible_matches: List[str] = self._wordtree.find_words(word_decoded)
        # TODO: finish this

    def _get_first_incomplete_word(self,
                                   coded_list: List[str],
                                   decoded_list: List[str]) -> Tuple[str, str]:
        for i in range(len(coded_list)):
            if "_" in decoded_list[i]:
                return coded_list[i], decoded_list[i]
        return "", ""


# class Puzzle:
#     """
#     Data type for cryptoquote puzzle
#     :param coding_dict: dict of coded letters and matching decoded letters
#     :param coded_quote_words: list of original words in cryptoquote
#     :param decoded_quote_words: list of words being decoded (* = unknown letter)
#     :param coded_author_words: list of words in author part of cryptoquote
#     :param decoded_author_words: list of author part words being decoded
#     """
#
#     def __init__(self,
#                  coding_dict: Dict[str, str],
#                  coded_quote_words: List[str],
#                  decoded_quote_words: List[str],
#                  coded_author_words: Optional[List[str]] = None,
#                  decoded_author_words: Optional[List[str]] = None
#                  ) -> None:
#         self.coding_dict = coding_dict
#         self.coded_quote_words = coded_quote_words
#         self.decoded_quote_words = decoded_quote_words
#         self.coded_author_words = coded_author_words
#         self.decoded_author_words = decoded_author_words
#
#     def is_solved(self) -> bool:
#         """
#         Returns true if all letters have been decoded
#         Only works if PuzzleTree only makes new Puzzles with real English words
#         """
#         for value in self.coding_dict.values():
#             if value == UNKNOWN:
#                 return False
#         return True
#
#     def get_solution_string(self) -> str:
#         """
#         Converts decoded quote/author word lists into single string
#         """
#         author_string: str = ""
#         quote_string: str = self.word_list_to_string(self.decoded_quote_words)
#         if self.decoded_author_words is not None:
#             author_string = " - " + self.word_list_to_string(
#                 self.decoded_author_words
#             )
#         return quote_string + author_string
#
#     @staticmethod
#     def word_list_to_string(word_list: List[str]) -> str:
#         """
#         Converts word list to string, respecting spacing around punctuation
#         :param word_list: list of words (with punctuation)
#         :return: sentence string with proper spacing
#
#         >>> Puzzle.word_list_to_string(
#         ...     ['HELLO', ',', "I'M", 'A', 'STRING', '!'])
#         "HELLO, I'M A STRING!"
#         """
#         return_string: str = ""
#         space: str = " "
#         for word in word_list:
#             if re.match(r"[,.!]", word):
#                 return_string = return_string + word
#             else:
#                 return_string = return_string + space + word
#         return return_string.lstrip(space)
#
#     def get_next_word_to_decode(self) -> List[Union[int, str]]:
#         """
#         Returns next quote word to decode,
#             based on number of remaining unknown letters
#             Words with apostrophes count as less unknown letters
#             Words from author part are not chosen
#         :returns (word index, chosen undecoded word)
#         """
#         # TODO: take out apostrophe bonus, just go with undecoded number
#         smallest_unknown: int = 50
#         chosen_word: str = ""
#         chosen_index: int = 0
#         for i in range(len(self.decoded_quote_words)):
#             curr_word: str = self.decoded_quote_words[i]
#             curr_unknown: int = self.count_unknown_letters(
#                 curr_word
#             )
#             if curr_unknown > 0 and curr_unknown < smallest_unknown:
#                 chosen_index = i
#                 chosen_word = curr_word
#                 smallest_unknown = curr_unknown
#         return [chosen_index, chosen_word]
#
#     @staticmethod
#     def count_unknown_letters(word: str) -> int:
#         """
#         Returns count of chars in word matching UNKNOWN char
#             Presence of ' reduces count
#         :param word: cryptoquote word, may be undecoded
#         :return: adjusted count of UNKNOWN char in word
#
#         >>> Puzzle.count_unknown_letters("T**")
#         2
#         >>> Puzzle.count_unknown_letters("THE")
#         0
#         >>> Puzzle.count_unknown_letters("**'*")
#         2
#         """
#         apos_bonus: int = 1
#         if (word.count("'") > 0):
#             return word.count(UNKNOWN) - apos_bonus
#         else:
#             return word.count(UNKNOWN)
#
#
# class PuzzleTree:
#     """
#     Data type for puzzle tree
#     Holds puzzle worklist, generates child states of given puzzle
#     :param coded_quote: quote portion of cryptoquote
#     :param coded_author: optional author portion of cryptoquote
#     """
#
#     def __init__(self,
#                  coded_quote: str,
#                  coded_author: str = None,
#                  corpus_file_path: str = None) -> None:
#         if corpus_file_path is not None:
#             self.lang_model: WordPatterns = WordPatterns(corpus_file_path)
#         else:
#             self.lang_model: WordPatterns = WordPatterns()
#         # TODO: Worklist should be list of coding dictionaries!
#         #       All puzzles have same starting coded words
#         #       Decoded words can be generated from coded words and coding dict
#         #       Might be easier to update worklist with dicts than new puzzles?
#         self.worklist: List[Puzzle] = []
#         self.worklist.append(
#             self.make_inital_puzzle(coded_quote, coded_author)
#         )
#
#     def make_inital_puzzle(self,
#                            coded_quote: str,
#                            coded_author: str = None) -> Puzzle:
#         coded_quote_words = self.string_to_caps_words(coded_quote)
#         decoded_quote_words = self.init_decoded_words(coded_quote_words)
#         coding_dict = self.init_coding_dict()
#         if coded_author is not None:
#             coded_author_words = self.string_to_caps_words(
#                 coded_author
#             )
#             decoded_author_words = self.init_decoded_words(coded_author_words)
#             puzzle = Puzzle(coding_dict, coded_quote_words, decoded_quote_words,
#                             coded_author_words, decoded_author_words)
#             return puzzle
#         else:
#             puzzle = Puzzle(coding_dict, coded_quote_words, decoded_quote_words)
#             return puzzle
#
#     def make_child_puzzles(self,
#                            puzzle: Puzzle) -> None:
#         """
#         Generates new Puzzles with new matched word
#             and adds to start of worklist
#         :param puzzle: starting puzzle
#         """
#         # TODO: I changed this method at some point, but docs are the same
#         #       How does it actually work now?
#         new_puzzle_list: List[Puzzle] = []
#         next_word: List[Union[int, str]] = \
#             puzzle.get_next_word_to_decode()
#         next_word_index: int = next_word[0]
#         matches: List[List[str]] = self.lang_model.get_possible_word_matches(
#             next_word[1]
#         )
#         for match in matches:
#             # copies are needed here to avoid mutating the parent,
#             # so all child puzzles start from the same parent puzzle
#             coding_dict: Dict[str, str] = puzzle.coding_dict.copy()
#             coded_quote_words: List[str] = \
#                 puzzle.coded_quote_words.copy()
#             decoded_quote_words: List[str] = \
#                 puzzle.decoded_quote_words.copy()
#             decoded_word: str = decoded_quote_words[next_word_index]
#             coded_word: str = coded_quote_words[next_word_index]
#             i_of_unknowns: List[int] = self.find_indices_of_unknown(
#                 decoded_word
#             )
#             conflict_flag: bool = False
#             for i in range(len(i_of_unknowns)):
#                 coded_char: str = coded_word[i_of_unknowns[i]]
#                 decoded_char: str = match[i]
#                 if coding_dict[coded_char] == UNKNOWN:
#                     coding_dict[coded_char] = decoded_char
#                 else:
#                     conflict_flag = True
#                     break
#             # skip to next match if there's a conflict
#             if not conflict_flag:
#                 decoded_quote_words = self.make_new_decoded_words(
#                     coding_dict, coded_quote_words
#                 )
#                 # TODO: Need to check that all fully decoded words are valid
#                 #       Skip if not
#                 for word in decoded_quote_words:
#                     # check if valid
#                     # if not valid, conflict flag to True and break
#                     if not self.lang_model.is_valid_word(word):
#                         conflict_flag = True
#                     if conflict_flag:
#                         break
#                 if not conflict_flag:
#                     if puzzle.coded_author_words is None:
#                         new_puzzle: Puzzle = Puzzle(coding_dict,
#                                                     coded_quote_words,
#                                                     decoded_quote_words)
#                         new_puzzle_list = new_puzzle_list + [new_puzzle]
#                     else:
#                         coded_author_words = puzzle.coded_author_words.copy()
#                         decoded_author_words = self.make_new_decoded_words(
#                             coding_dict, coded_author_words)
#                         new_puzzle: Puzzle = Puzzle(coding_dict,
#                                                     coded_quote_words,
#                                                     decoded_quote_words,
#                                                     coded_author_words,
#                                                     decoded_author_words)
#                         new_puzzle_list = new_puzzle_list + [new_puzzle]
#         self.worklist = new_puzzle_list + self.worklist
#
#     @staticmethod
#     def string_to_caps_words(in_string: str) -> List[str]:
#         """
#         Convert string to list of words in caps
#         :param in_string: input string
#         :return: word list (all caps)
#
#         >>> PuzzleTree.string_to_caps_words("Svool, R'n z hgirmt!")
#         ['SVOOL', ',', "R'N", 'Z', 'HGIRMT', '!']
#         """
#         return re.findall(r"[\w']+|[.,!?;]", in_string.upper())
#
#     @staticmethod
#     def init_decoded_words(in_words: List[str]) -> List[str]:
#         """
#         Given coded words list, produce initial decoded words list
#             (all words and punctuation copied, but with letter placeholders)
#         :param in_words: coded words list
#         :return: decoded words list (with letter placeholders)
#
#         >>> PuzzleTree.init_decoded_words(
#         ...     ['SVOOL', ',', "R'N", 'Z', 'HGIRMT', '!']
#         ... )
#         ['*****', ',', "*'*", '*', '******', '!']
#         """
#         output_words = []
#         for word in in_words:
#             output_word = ""
#             for char in word:
#                 if char.isalpha():
#                     output_word += UNKNOWN
#                 else:
#                     output_word += char
#             output_words.append(output_word)
#         return output_words
#
#     @staticmethod
#     def init_coding_dict() -> Dict[str, str]:
#         """
#         Produce blank coding dictionary
#             keys: capital letters
#             values: * placeholder
#         :return: blank coding dictionary
#
#         >>> PuzzleTree.init_coding_dict() #doctest: +ELLIPSIS
#         {'A': '*', 'B': '*', 'C': '*', ... 'Z': '*'}
#         """
#         blank_coding_dict = {}
#         uppercase_list = list(string.ascii_uppercase)
#         for letter in uppercase_list:
#             blank_coding_dict[letter] = UNKNOWN
#         return blank_coding_dict
#
#     def get_next_puzzle_from_worklist(self) -> Puzzle:
#         """
#         Gets and removes next puzzle from worklist
#         :return: next puzzle in worklist
#         """
#         return self.worklist.pop(0)
#
#     @staticmethod
#     def find_indices_of_unknown(decoded_word: str) -> List[int]:
#         """
#         Finds indices of UNKNOWN chars in word
#         :param decoded_word: word with UNKNOWN chars
#
#         >>> PuzzleTree.find_indices_of_unknown("*HI*")
#         [0, 3]
#         >>> PuzzleTree.find_indices_of_unknown("****")
#         [0, 1, 2, 3]
#         >>> PuzzleTree.find_indices_of_unknown("THIS")
#         []
#         """
#         return [m.start() for m in re.finditer(re.escape(UNKNOWN),
#                                                decoded_word)]
#
#     @staticmethod
#     def make_new_decoded_words(coding_dict: Dict[str, str],
#                                coded_words: List[str]) -> List[str]:
#         """
#         Produces word list with known letters decoded
#         :param coding_dict: dict of code, and matching decoded, letters
#         :param coded_words: cryptoquote converted to list form
#         :return decoded word list
#         """
#         decoded_words: List[str] = []
#         for word in coded_words:
#             decoded_word: str = ""
#             for char in word:
#                 if char.isalpha():
#                     decoded_word = decoded_word + coding_dict[char]
#                 else:
#                     decoded_word = decoded_word + char
#             decoded_words.append(decoded_word)
#         return decoded_words


def string_to_caps_words(in_string: str) -> List[str]:
    """
    Convert string to list of words in caps
    :param in_string: input string
    :return: word list (all caps)

    >>> string_to_caps_words("Svool, R'n z hgirmt!")
    ['SVOOL', ',', "R'N", 'Z', 'HGIRMT', '!']
    """
    return re.findall(r"[\w'-]+|[.,!?;]", in_string.upper())
    # regex explanation:
    # first [] matches words, including "in-word punctuation" ie. ' and -
    # second bracket matches exactly 1 "non-word punctuation"
    # | == OR
    # so regex splits into words (via findall)


# def get_blank_cypherletter_map() -> Dict[str, Optional[List[str]]]:
#     # return {
#     #     'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [],
#     #     'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [], 'O': [], 'P': [],
#     #     'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [],
#     #     'Y': [], 'Z': [],
#     # }
#     retval: Dict[str, Optional[List[str]]] = {}
#     for letter in LETTERS:
#         retval[letter] = None
#     return retval
#
#
# def add_letters_to_mapping(cypherletter_map: Dict[str, Optional[List[str]]],
#                            word: str,
#                            match: str) -> Dict[str, List[str]]:
#     cypherletter_map = copy.deepcopy(cypherletter_map)
#     for i in range(len(word)):
#         if match[i] not in PUNCTUATION:
#             if cypherletter_map[word[i]] is None:
#                 cypherletter_map[word[i]] = [match[i]]
#             elif match[i] not in cypherletter_map[word[i]]:
#                 cypherletter_map[word[i]].append(match[i])
#     return cypherletter_map
#
#
# def intersect_mappings(map_a: Dict[str, Optional[List[str]]],
#                        map_b: Dict[str, Optional[List[str]]]) -> Dict[
#     str, Optional[List[str]]]:
#     intersected_map = get_blank_cypherletter_map()
#     for letter in LETTERS:
#         if map_a[letter] is None:
#             intersected_map[letter] = copy.deepcopy(map_b[letter])
#         elif map_b[letter] is None:
#             intersected_map[letter] = copy.deepcopy(map_a[letter])
#         else:
#             for mapped_letter in map_a[letter]:
#                 if mapped_letter in map_b[letter]:
#                     if intersected_map[letter] is None:
#                         intersected_map[letter] = [mapped_letter]
#                     else:
#                         intersected_map[letter].append(mapped_letter)
#     return intersected_map
#
#
# def remove_solved_letters_from_map(cypherletter_map: Dict[str, List[str]]) \
#     -> Dict[str, List[str]]:
#     except_message: str = "A code letter was left with no possible solution"
#     cypherletter_map = copy.deepcopy(cypherletter_map)
#     done: bool = False
#     while not done:
#         done = True  # assume done
#
#         # scan through map and track solved letters
#         solved_letters = []
#         for letter in LETTERS:
#             if cypherletter_map[letter] is not None \
#                 and len(cypherletter_map[letter]) == 1:
#                 if cypherletter_map[letter][0] in solved_letters:
#                     # 2 code letters with same letter mapping = no solution
#                     raise ValueError(except_message)
#                 else:
#                     solved_letters.append(cypherletter_map[letter][0])
#
#         # removed solved letters as possibilities for other letters
#         for letter in LETTERS:
#             for solved in solved_letters:
#                 if cypherletter_map[letter] is not None:
#                     if len(cypherletter_map[letter]) != 1 \
#                         and (solved in cypherletter_map[letter]):
#                         cypherletter_map[letter].remove(solved)
#                         if len(cypherletter_map[letter]) == 1:
#                             # new letter is now solved, so we're not done yet!
#                             done = False
#                         elif len(cypherletter_map[letter]) == 0:
#                             raise ValueError(except_message)
#                     elif len(cypherletter_map[letter]) == 0:
#                         raise ValueError(except_message)
#                 else:
#                     # replace with all letters,
#                     # then remove this letter and solved letter
#                     cypherletter_map[letter] = [
#                         char for char in LETTERS if char not in [letter,
#                                                                  solved]]
#
#     return cypherletter_map


def decrypt_with_cypherletter_map(
    code: str,
    cypherletter_map: CypherLetterMap) -> str:
    code = code.upper()
    decoded: List[str] = list(copy.deepcopy(code))
    for i in range(len(code)):
        letter: str = code[i]
        if letter in LETTERS:  # is it an A-Z letter?
            match: Optional[List[str]] = \
                cypherletter_map.get_letter_for_cypher(letter)
            if match is not None and len(match) == 1:
                decoded[i] = match[0]
            else:
                decoded[i] = "_"
    return "".join(decoded)


# def get_cypherletter_map_as_string(
#     cypherletter_map: Dict[str, List[str]]) -> str:
#     key: List[str] = []
#     for letter in LETTERS:
#         if cypherletter_map[letter] is None \
#             or len(cypherletter_map[letter]) != 1:
#             key.append("_")
#         else:
#             key.append(cypherletter_map[letter][0])
#     return "Decoder:\n{0}\n{1}".format(LETTERS, "".join(key))


def is_quote_solved(cypherletter_map: Dict[str, Optional[List[str]]]) -> bool:
    # TODO: make unit tests
    # TODO: develop this
    return False  # stub


def decrypt_quote(coded_quote: str,
                  coded_author: str = None,
                  print_cypher: bool = False) -> str:
    # TODO: may need to make path absolute
    pattern_dict_file_path = os.path.join(
        os.path.dirname(__file__), PATTERNS_JSON)
    corpus_file_path = os.path.join(
        os.path.dirname(__file__), CORPUS_FILE)
    # TODO: put this back once testing works
    # word_patterns = WordPatterns(pattern_dict_file_path,
    #                                corpus_file_path=corpus_file_path)
    word_patterns = WordPatterns(pattern_dict_file_path,
                                 True,
                                 corpus_file_path)
    final_map: CypherLetterMap = CypherLetterMap()
    quote_words: List[str] = string_to_caps_words(coded_quote)
    for word in quote_words:
        new_map: CypherLetterMap = CypherLetterMap()
        matches: List[str] = word_patterns.code_word_to_match_words(word)
        # add possible decryption letters to cypherletters
        if len(matches) == 0:
            continue
        for match in matches:
            new_map.add_letters_to_mapping(word, match)
        final_map.intersect_mappings(new_map)
    final_map.remove_solved_letters_from_map(final_map)
    decoded_quote: str = decrypt_with_cypherletter_map(coded_quote, final_map)
    # TODO: if quote isn't yet solved, run through SolutionTree
    return_value: str = ""
    if coded_author is None:
        return_value = decoded_quote
        # return "{0}\n{1}".format(decoded_quote, get_cypherletter_map_as_string(final_map))
    else:
        decoded_author: str = decrypt_with_cypherletter_map(coded_author,
                                                            final_map)
        return_value = "{0} - {1}".format(decoded_quote, decoded_author)
    if (print_cypher):
        return "{0}\n{1}".format(
            return_value, get_cypherletter_map_as_string(final_map))
    else:
        return return_value

    # puzzle_tree = PuzzleTree(coded_quote, coded_author, "words_alpha_apos.txt")
    # # genrec search tree loop with worklist (?)
    # while True:
    #     try:
    #         current_puzzle: Puzzle = puzzle_tree.get_next_puzzle_from_worklist()
    #     except IndexError:
    #         return "Puzzle could not be solved"
    #     # TODO: remove this when app works
    #     print(current_puzzle.get_solution_string())
    #     if current_puzzle.is_solved():
    #         return current_puzzle.get_solution_string()
    #     else:
    #         #   If not, make any possible children
    #         #   and append to front of worklist
    #         puzzle_tree.make_child_puzzles(
    #             current_puzzle
    #         )


# TODO: add command line arguments to:
#       update patterns dict from corpus file
#       update corpus file from patterns dict
#       suggest words (and have them added to patterns dict if solution works)
#       force add words to patterns dict
if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    quote: str = "Lz lv we aorbvtqr znbz we inlohqry bqr mqrr byh " \
                 "nbaae, byh tyqrvzqblyrh ge abqryzzbo zeqbyye. Osjr " \
                 "lv znr inbly cnrqrge zs glyh b inloh zs lzv abqryzv."
    print(decrypt_quote(quote))
