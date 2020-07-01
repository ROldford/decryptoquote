# -*- coding: utf-8 -*-

"""Main module."""

import os
import re
import string
from typing import Dict, List, Optional, Union

UNKNOWN: str = "*"
CORPUS_FILE: str = "words_alpha_apos.txt"
SHORT_WORDS_CORPUS_FILE: str = "words_small.txt"


# TODO: Use word pattern concept in
#      https://inventwithpython.com/hacking/chapter18.html


class LanguageModel:
    def __init__(self,
                 main_file_path: str = CORPUS_FILE) -> None:
        """
        Create LanguageModel instance from given corpus file
            corpus file is large file of English text, .txt format
        :param main_file_path: path to language corpus file
        :exception IOError if corpus file is invalid
        """
        # TODO: enforce Singleton?
        main_file_path = os.path.join(
            os.path.dirname(__file__), main_file_path)
        self._patterns: Dict[str, List[str]] = {}
        try:
            with open(main_file_path, 'r') as file:
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
                f"Language model file not valid: {main_file_path}"
            ) from err

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
            if letter not in "'-":
                if letter not in letter_nums:
                    letter_nums[letter] = str(pattern_num)
                    pattern_num += 1
                word_pattern.append(letter_nums[letter])
            else:
                word_pattern.append(letter)
        return ".".join(word_pattern)

    def pattern_to_match_words(self, pattern: str) -> List[str]:
        return self._patterns[pattern]

    def code_word_to_match_words(self, code_word: str) -> List[str]:
        pattern: str = self.word_to_pattern(code_word)
        return self.pattern_to_match_words(pattern)


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
        self.coding_dict = coding_dict
        self.coded_quote_words = coded_quote_words
        self.decoded_quote_words = decoded_quote_words
        self.coded_author_words = coded_author_words
        self.decoded_author_words = decoded_author_words

    def is_solved(self) -> bool:
        """
        Returns true if all letters have been decoded
        Only works if PuzzleTree only makes new Puzzles with real English words
        """
        for value in self.coding_dict.values():
            if value == UNKNOWN:
                return False
        return True

    def get_solution_string(self) -> str:
        """
        Converts decoded quote/author word lists into single string
        """
        author_string: str = ""
        quote_string: str = self.word_list_to_string(self.decoded_quote_words)
        if self.decoded_author_words is not None:
            author_string = " - " + self.word_list_to_string(
                self.decoded_author_words
            )
        return quote_string + author_string

    @staticmethod
    def word_list_to_string(word_list: List[str]) -> str:
        """
        Converts word list to string, respecting spacing around punctuation
        :param word_list: list of words (with punctuation)
        :return: sentence string with proper spacing

        >>> Puzzle.word_list_to_string(
        ...     ['HELLO', ',', "I'M", 'A', 'STRING', '!'])
        "HELLO, I'M A STRING!"
        """
        return_string: str = ""
        space: str = " "
        for word in word_list:
            if re.match(r"[,.!]", word):
                return_string = return_string + word
            else:
                return_string = return_string + space + word
        return return_string.lstrip(space)

    def get_next_word_to_decode(self) -> List[Union[int, str]]:
        """
        Returns next quote word to decode,
            based on number of remaining unknown letters
            Words with apostrophes count as less unknown letters
            Words from author part are not chosen
        :returns (word index, chosen undecoded word)
        """
        # TODO: take out apostrophe bonus, just go with undecoded number
        smallest_unknown: int = 50
        chosen_word: str = ""
        chosen_index: int = 0
        for i in range(len(self.decoded_quote_words)):
            curr_word: str = self.decoded_quote_words[i]
            curr_unknown: int = self.count_unknown_letters(
                curr_word
            )
            if curr_unknown > 0 and curr_unknown < smallest_unknown:
                chosen_index = i
                chosen_word = curr_word
                smallest_unknown = curr_unknown
        return [chosen_index, chosen_word]

    @staticmethod
    def count_unknown_letters(word: str) -> int:
        """
        Returns count of chars in word matching UNKNOWN char
            Presence of ' reduces count
        :param word: cryptoquote word, may be undecoded
        :return: adjusted count of UNKNOWN char in word

        >>> Puzzle.count_unknown_letters("T**")
        2
        >>> Puzzle.count_unknown_letters("THE")
        0
        >>> Puzzle.count_unknown_letters("**'*")
        2
        """
        apos_bonus: int = 1
        if (word.count("'") > 0):
            return word.count(UNKNOWN) - apos_bonus
        else:
            return word.count(UNKNOWN)


class PuzzleTree:
    """
    Data type for puzzle tree
    Holds puzzle worklist, generates child states of given puzzle
    :param coded_quote: quote portion of cryptoquote
    :param coded_author: optional author portion of cryptoquote
    """

    def __init__(self,
                 coded_quote: str,
                 coded_author: str = None,
                 corpus_file_path: str = None) -> None:
        if corpus_file_path is not None:
            self.lang_model: LanguageModel = LanguageModel(corpus_file_path)
        else:
            self.lang_model: LanguageModel = LanguageModel()
        # TODO: Worklist should be list of coding dictionaries!
        #       All puzzles have same starting coded words
        #       Decoded words can be generated from coded words and coding dict
        #       Might be easier to update worklist with dicts than new puzzles?
        self.worklist: List[Puzzle] = []
        self.worklist.append(
            self.make_inital_puzzle(coded_quote, coded_author)
        )

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

    def make_child_puzzles(self,
                           puzzle: Puzzle) -> None:
        """
        Generates new Puzzles with new matched word
            and adds to start of worklist
        :param puzzle: starting puzzle
        """
        # TODO: I changed this method at some point, but docs are the same
        #       How does it actually work now?
        new_puzzle_list: List[Puzzle] = []
        next_word: List[Union[int, str]] = \
            puzzle.get_next_word_to_decode()
        next_word_index: int = next_word[0]
        matches: List[List[str]] = self.lang_model.get_possible_word_matches(
            next_word[1]
        )
        for match in matches:
            # copies are needed here to avoid mutating the parent,
            # so all child puzzles start from the same parent puzzle
            coding_dict: Dict[str, str] = puzzle.coding_dict.copy()
            coded_quote_words: List[str] = \
                puzzle.coded_quote_words.copy()
            decoded_quote_words: List[str] = \
                puzzle.decoded_quote_words.copy()
            decoded_word: str = decoded_quote_words[next_word_index]
            coded_word: str = coded_quote_words[next_word_index]
            i_of_unknowns: List[int] = self.find_indices_of_unknown(
                decoded_word
            )
            conflict_flag: bool = False
            for i in range(len(i_of_unknowns)):
                coded_char: str = coded_word[i_of_unknowns[i]]
                decoded_char: str = match[i]
                if coding_dict[coded_char] == UNKNOWN:
                    coding_dict[coded_char] = decoded_char
                else:
                    conflict_flag = True
                    break
            # skip to next match if there's a conflict
            if not conflict_flag:
                decoded_quote_words = self.make_new_decoded_words(
                    coding_dict, coded_quote_words
                )
                # TODO: Need to check that all fully decoded words are valid
                #       Skip if not
                for word in decoded_quote_words:
                    # check if valid
                    # if not valid, conflict flag to True and break
                    if not self.lang_model.is_valid_word(word):
                        conflict_flag = True
                    if conflict_flag:
                        break
                if not conflict_flag:
                    if puzzle.coded_author_words is None:
                        new_puzzle: Puzzle = Puzzle(coding_dict,
                                                    coded_quote_words,
                                                    decoded_quote_words)
                        new_puzzle_list = new_puzzle_list + [new_puzzle]
                    else:
                        coded_author_words = puzzle.coded_author_words.copy()
                        decoded_author_words = self.make_new_decoded_words(
                            coding_dict, coded_author_words)
                        new_puzzle: Puzzle = Puzzle(coding_dict,
                                                    coded_quote_words,
                                                    decoded_quote_words,
                                                    coded_author_words,
                                                    decoded_author_words)
                        new_puzzle_list = new_puzzle_list + [new_puzzle]
        self.worklist = new_puzzle_list + self.worklist

    @staticmethod
    def string_to_caps_words(in_string: str) -> List[str]:
        """
        Convert string to list of words in caps
        :param in_string: input string
        :return: word list (all caps)

        >>> PuzzleTree.string_to_caps_words("Svool, R'n z hgirmt!")
        ['SVOOL', ',', "R'N", 'Z', 'HGIRMT', '!']
        """
        return re.findall(r"[\w']+|[.,!?;]", in_string.upper())

    @staticmethod
    def init_decoded_words(in_words: List[str]) -> List[str]:
        """
        Given coded words list, produce initial decoded words list
            (all words and punctuation copied, but with letter placeholders)
        :param in_words: coded words list
        :return: decoded words list (with letter placeholders)

        >>> PuzzleTree.init_decoded_words(
        ...     ['SVOOL', ',', "R'N", 'Z', 'HGIRMT', '!']
        ... )
        ['*****', ',', "*'*", '*', '******', '!']
        """
        output_words = []
        for word in in_words:
            output_word = ""
            for char in word:
                if char.isalpha():
                    output_word += UNKNOWN
                else:
                    output_word += char
            output_words.append(output_word)
        return output_words

    @staticmethod
    def init_coding_dict() -> Dict[str, str]:
        """
        Produce blank coding dictionary
            keys: capital letters
            values: * placeholder
        :return: blank coding dictionary

        >>> PuzzleTree.init_coding_dict() #doctest: +ELLIPSIS
        {'A': '*', 'B': '*', 'C': '*', ... 'Z': '*'}
        """
        blank_coding_dict = {}
        uppercase_list = list(string.ascii_uppercase)
        for letter in uppercase_list:
            blank_coding_dict[letter] = UNKNOWN
        return blank_coding_dict

    def get_next_puzzle_from_worklist(self) -> Puzzle:
        """
        Gets and removes next puzzle from worklist
        :return: next puzzle in worklist
        """
        return self.worklist.pop(0)

    @staticmethod
    def find_indices_of_unknown(decoded_word: str) -> List[int]:
        """
        Finds indices of UNKNOWN chars in word
        :param decoded_word: word with UNKNOWN chars

        >>> PuzzleTree.find_indices_of_unknown("*HI*")
        [0, 3]
        >>> PuzzleTree.find_indices_of_unknown("****")
        [0, 1, 2, 3]
        >>> PuzzleTree.find_indices_of_unknown("THIS")
        []
        """
        return [m.start() for m in re.finditer(re.escape(UNKNOWN),
                                               decoded_word)]

    @staticmethod
    def make_new_decoded_words(coding_dict: Dict[str, str],
                               coded_words: List[str]) -> List[str]:
        """
        Produces word list with known letters decoded
        :param coding_dict: dict of code, and matching decoded, letters
        :param coded_words: cryptoquote converted to list form
        :return decoded word list
        """
        decoded_words: List[str] = []
        for word in coded_words:
            decoded_word: str = ""
            for char in word:
                if char.isalpha():
                    decoded_word = decoded_word + coding_dict[char]
                else:
                    decoded_word = decoded_word + char
            decoded_words.append(decoded_word)
        return decoded_words


def decrypt_quote(coded_quote: str, coded_author: str = None) -> str:
    puzzle_tree = PuzzleTree(coded_quote, coded_author, "words_alpha_apos.txt")
    # genrec search tree loop with worklist (?)
    while True:
        try:
            current_puzzle: Puzzle = puzzle_tree.get_next_puzzle_from_worklist()
        except IndexError:
            return "Puzzle could not be solved"
        # TODO: remove this when app works
        print(current_puzzle.get_solution_string())
        if current_puzzle.is_solved():
            return current_puzzle.get_solution_string()
        else:
            #   If not, make any possible children
            #   and append to front of worklist
            puzzle_tree.make_child_puzzles(
                current_puzzle
            )


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    coded_quote: str = "Lz lv we aorbvtqr znbz we inlohqry bqr mqrr byh " \
                       "nbaae, byh tyqrvzqblyrh ge abqryzzbo zeqbyye. Osjr " \
                       "lv znr inbly cnrqrge zs glyh b inloh zs lzv abqryzv."
    print(decrypt_quote(coded_quote))
