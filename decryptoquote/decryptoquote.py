# -*- coding: utf-8 -*-

"""
Main module.
"""
# new idea
#   For each word in coded text, use WordPatterns to get possible pattern
#   matches, and put in list of lists
#   Each sub-list holds all possible pattern matches for that word
#   Also need main index counter and list of sub-list index counters
#   Main index counter gives index in main list where we try a possible match
#     this round
#   Each sub-index is index in sub-list of possible match to try this round
#   Main index and all sub-indices start at 0 (i.e. first word)
#   Also need simpler CypherLetterMap: Dict with coded letters as keys, value
#     is either None (no match yet) or matching decoded letter
#       Can also give currently decoded text
#   Then use backtracking search from first word to last:
#       Get list at main index, get word match at that list's sub-index
#       Check for mismatches
#           Mismatch = Any decoded
#       If no mismatches, update CypherLetterMap (which updates decoded message)
#         then increment main index
#       If mismatch, increment list's subindex
#       If subindex >= len(sub-list), backtrack:
#           Set current subindex to 0
#           Decrement main index
#           Increment that subindex
#       If main index >= len(main list), you have a valid solution!
import copy
import json
import os
import pprint
import re
import string
import logging
from typing import Dict, List, Optional, Union, Tuple

UNKNOWN: str = "*"
PATTERNS_JSON: str = "word_patterns.json"
CORPUS_FILE: str = "words_alpha_apos.txt"
# SHORT_WORDS_CORPUS_FILE: str = "words_small.txt"
IN_WORD_PUNCT: str = "'-"
NON_WORD_PUNCT: str = ".,!?;"
PUNCTUATION: str = "{0}{1}".format(IN_WORD_PUNCT, NON_WORD_PUNCT)
LETTERS: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS: str = "0123456789"
EXCEPT_MESSAGE: str = "A code letter was left with no possible solution"

logging.basicConfig(
    filename='decryptoquote.log',
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)


class WordPatterns:
    """
    This class organizes a set of English words by the pattern of distinct
    letters in each word. For example, "this" has the pattern "1.2.3.4", since
    each letter is distinct, as does "code", while "noon" has the pattern
    "1.2.2.1". Since Cryptoquotes use a substitution cypher, the coded and
    decoded words will have the same pattern. This can be used to determine
    which words are possible matches.

    :param saved_patterns_path: path to saved pattern file
    :param overwrite_json: if `True`, overwrites any existing saved patterns
      file
    :param corpus_file_path: path to language corpus file. This is required to
      make a new saved patterns file
    :exception IOError if corpus file is invalid
    """

    def __init__(self,
                 saved_patterns_path: str,
                 overwrite_json: bool = False,
                 corpus_file_path: str = None) -> None:
        self._saved_patterns_path = saved_patterns_path
        self._corpus_file_path: Optional[str] = corpus_file_path
        if overwrite_json or not os.path.exists(saved_patterns_path):
            # we need a new patterns JSON, so get words from corpus text file
            self._patterns: Dict[str, List[str]] = {}
            try:
                with open(corpus_file_path, 'r') as file:
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
                with open(saved_patterns_path, "w") as file:
                    json.dump(self._patterns, file)
            except Exception as err:
                raise IOError(
                    f"Patterns file not created correctly: "
                    f"{saved_patterns_path}"
                ) from err
        else:
            # just load patterns JSON
            with open(saved_patterns_path, "r") as file:
                self._patterns = json.load(file)

    @property
    def saved_patterns_path(self) -> str:
        return self._saved_patterns_path

    @property
    def corpus_file_path(self) -> Optional[str]:
        return self._corpus_file_path

    @staticmethod
    def word_to_pattern(word: str) -> str:
        """
        Determines the letter pattern for the word given. Each distinct letter
        is given a unique number, starting from 1 and counting up. If a letter
        occurs again, the original number is used. Numbers are separated by
        periods.

        For example, the pattern for the word "noon" is "1.2.2.1". We start
        with "n", designated with 1. We move on to "o", which gets 2. Since "o"
        appears again, we repeat the 2, and finish with 1 for "n".

        Apostrophes appear as themselves, not as numbers, but are still
        separated by periods. For example, "didn't" has the pattern
        "1.2.1.3.'.4".

        :param word: given word
        :return: pattern for that word
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
        """
        Determines all matching words for a given pattern in the word patterns
        database. Patterns are described in :meth:`word_to_pattern`.

        :param pattern: given word pattern
        :return: words matching that pattern, or an empty list if no matches
          exist
        """
        if pattern not in self._patterns:
            for character in pattern:
                if character in DIGITS:
                    return []
            return [pattern]
        else:
            return self._patterns[pattern]

    def code_word_to_match_words(self, code_word: str) -> List[str]:
        """
        Determines all words whose pattern matches that of the given code word,
        and could therefore possibly be the solution for that word.

        :param code_word: given code word
        :return: real words matching code word's letter pattern, or an empty
          list if no matches exist
        """
        pattern: str = self.word_to_pattern(code_word)
        return self.pattern_to_match_words(pattern)

    def add_new_words(self, words: List[str]):
        """
        Adds all words in the list to the stored patterns.

        :param words: words to add
        """
        for word in words:
            word_upper = word.upper()
            pattern = self.word_to_pattern(word_upper)
            matching_words = self.pattern_to_match_words(pattern)

            if word_upper not in matching_words:
                matching_words.append(word_upper)
                self._patterns[pattern] = matching_words

    def save_corpus_from_patterns(self, corpus_file_path: str) -> None:
        pass  # TODO: stub


class CypherLetterMap:
    """
    This class maps coded letters to matching decoded letters, or to `None` if
    no matching value has been determined.
    """

    def __init__(self):
        self._clmap: Dict[str, Optional[str]] = {}
        self._past_coded_words: List[Tuple[str, str]] = []  # coded, decoded
        for letter in LETTERS:
            self._clmap[letter] = None

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self._clmap!r})')

    def __str__(self):
        key: List[str] = []
        for letter in LETTERS:
            if self._clmap[letter] is None:
                key.append("_")
            else:
                key.append(self._clmap[letter])
        return f"Decoder:\n{LETTERS}\n{''.join(key)}"

    def __eq__(self, other):
        try:
            if self is other:
                return True
            else:
                for key in self._clmap.keys():
                    if self.get_letter_for_cypher(key) \
                        != other.get_letter_for_cypher(key):
                        return False
                return True
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_letter_for_cypher(self, coded_letter: str) -> Optional[str]:
        """
        Get the matching decoded letter for the given coded letter

        :param coded_letter: given coded letter
        :return: matching decoded letter, or `None` if no match
        """
        return self._clmap[coded_letter.upper()]

    def decode(self, coded_text: str) -> str:
        """
        Decrypts coded text based on current cypher letter map. If coded
        letters do not have decoded matches, the underscore ("_") will be used
        in its place.

        :param coded_text: coded text to decrypt
        :return: decrypted version of coded text, which may have underscores if
          letters are not decoded
        """
        decoded_text = []
        for letter in coded_text.upper():
            if letter in self._clmap.keys():
                if self._clmap[letter] is None:
                    decoded_text.append('_')
                else:
                    decoded_text.append(self._clmap[letter])
            else:
                decoded_text.append(letter)
        return "".join(decoded_text)

    def add_word_to_mapping(self,
                            coded_word: str,
                            decoded_word: str):
        """
        Updates the cypher letter map using the given coded word and its
        decoded form.

        :param coded_word: word from coded puzzle to add
        :param decoded_word: matching decoded word
        """
        coded_word, decoded_word = self._validate_words(coded_word,
                                                        decoded_word)
        self._past_coded_words.append((coded_word, decoded_word))
        self._add_word_to_mapping_no_save(coded_word, decoded_word)

    def remove_last_word_from_mapping(self):
        """
        Updates the cypher letter dictionary by undoing the last word addition.
        """
        # current strategy: remove last word, clear map, rebuild
        # could be costly?
        # possible improvement: also store number of "codings"
        #   ie. number of times we see that coded/decoded letter pair
        # reduce that number each time we remove
        # only remove letter when codings count <= 0
        self._past_coded_words = self._past_coded_words[:-1]  # remove last
        for letter in self._clmap.keys():
            self._clmap[letter] = None  # clear cl_map
        for word_pair in self._past_coded_words:
            coded_word, decoded_word = word_pair
            self._add_word_to_mapping_no_save(coded_word, decoded_word)

    def does_word_coding_work(
        self,
        coded_word: str,
        possible_decoded_word: str
    ) -> bool:
        """
        Checks if this "word coding", or pair of coded word and possible
        matching decoded word, can be safely added to the mapping without
        causing coding inconsistencies. Coding inconsistencies include:

            * Mapping a coded letter that already has a matching decoded letter
              to a new letter
            * Adding a decoded letter that already exists in the mapping

        :param coded_word: coded word to check
        :param possible_decoded_word: possible decoded word to check
        :return: True if coded word and possible decoded word could be safely
          added to the mapping
        """
        try:
            word_pair = self._validate_words(coded_word, possible_decoded_word)
        except ValueError:
            return False
        coded_word, possible_decoded_word = word_pair
        for letter_pair in zip(coded_word, possible_decoded_word):
            coded_letter, decoded_letter = letter_pair
            if coded_letter in PUNCTUATION or coded_letter == "'":
                if decoded_letter == coded_letter:
                    continue
                else:
                    return False
            if self._clmap[coded_letter] is None:
                if decoded_letter in self._clmap.values():
                    return False
                if decoded_letter in PUNCTUATION:
                    return False
            else:
                if self._clmap[coded_letter] != decoded_letter:
                    return False
        return True

    def clear(self):
        self._past_coded_words: List[Tuple[str, str]] = []  # coded, decoded
        for letter in LETTERS:
            self._clmap[letter] = None

    def _add_word_to_mapping_no_save(self,
                                     coded_word: str,
                                     decoded_word: str):
        coded_word, decoded_word = self._validate_words(coded_word,
                                                        decoded_word)
        word_matches = zip(coded_word, decoded_word)
        for letter_match in word_matches:
            coded_letter, decoded_letter = letter_match
            if coded_letter not in PUNCTUATION \
                and decoded_letter not in PUNCTUATION:
                # pair exists in map: no action
                if self._clmap[coded_letter] == decoded_letter:
                    continue
                # old key, new value
                if self._clmap[coded_letter] is not None:
                    raise ValueError(
                        f"Coded letter {coded_letter} already has a match")
                # same value for 2 keys
                if decoded_letter in self._clmap.values():
                    raise ValueError(
                        f"Decoded letter {decoded_letter} is already mapped to "
                        f"another coded letter")
                self._clmap[coded_letter] = decoded_letter
            else:
                if coded_letter != decoded_letter:
                    raise ValueError(
                        f"Coded word {coded_word} and decoded word {decoded_word} "
                        f"have different punctuation locations")

    def _validate_words(self,
                        coded_word: str,
                        decoded_word: str):
        """
        Ensures that coded and decoded words are uppercase and of equal length.

        :param coded_word: coded word to check
        :param decoded_word: decoded word to check
        :return: coded and decoded words in upper case
        :raises ValueError: if words have different lengths
        """
        if len(coded_word) != len(decoded_word):
            raise ValueError("Coded and decoded words must "
                             "have the same length")
        return coded_word.upper(), decoded_word.upper()


class Decrypter:
    """
    This class performs Cryptoquote decryption using a version of backtracking
    search.

    This version of backtracking search uses word pattern matches, as described
    in :class:`WordPatterns`. Decrypter determines all matches for each word in
    the coded text. It also maintains a master index value :math:`i` and an
    index value for each word :math:`j_x`. The algorithm works as follows:

    1. Initially, set :math:`i` and all :math:`j_x` to 0
    2. Select the "match word" :math:`j_i` for word :math:`i`
    3. Check that this match word is consistent with the current cypher-letter
      map (i.e. any coded letters, if decoded in the map, should decode to the
      same letter in the match word). If it is consistent, complete the "good
      match" steps. If not, complete the "bad match" steps.
    4. "Good match" steps

        a. Update the cypher letter map using the match word.
        b. Increment :math:`i`
        c. If :math:`i` >= number of words in the coded text, decrypting was
           successful; return `True`.
        d. Otherwise, return to step 2 and repeat.

    5. "Bad match" steps

        a. Increment :math:`j_i`
        b. If :math:`j_i` >= number of matches for word :math:`i`, follow the
          "backtrack" steps.
        c. Otherwise, return to step 2 and repeat.

    6. "Backtrack" steps

        a. Remove the match word from the cypher-letter map
        b. Set :math:`j_i` to 0
        c. Decrement :math:`i`
        d. Repeat "bad match" steps with new :math:`i`
        e. If :math:`i` < 0, no decoded text can be found; return `False`.
        f. Otherwise, return to step 2 and repeat.

    :param coded_text: the text to decode
    :param cypher_letter_map: CypherLetterMap to use. This map will be cleared
      before use.
    :param word_patterns: WordPatterns to use.

    .. attribute:: cypher_letter_map
        :type: CypherLetterMap
        :value: blank CypherLetterMap

            The mapping from coded cypher letters to decoded letters.
    """

    def __init__(
        self,
        coded_text: str,
        cypher_letter_map: CypherLetterMap,
        word_patterns: WordPatterns,
    ):
        self.cypher_letter_map = cypher_letter_map
        self.cypher_letter_map.clear()
        self._coded_words: List[str] = string_to_caps_words(coded_text)

        self._pattern_matches: List[List[str]] = []
        for coded_word in self._coded_words:
            matches = word_patterns.code_word_to_match_words(coded_word)
            self._pattern_matches.append(matches)

        self._word_index = 0
        self._match_indices = [0 for _ in self._coded_words]

    def decrypt(self) -> bool:
        """
        Decodes the cypher, returning a success value.

        The cypher-letter map can now be used to decode the Cryptoquote text.

        :return: `True` if decoding was successful
        """
        logging.debug("Starting new decryption...")
        word_count: int = len(self._coded_words)
        logging.debug(word_count)
        backtracking: bool = False
        while 0 <= self._word_index < word_count:
            if backtracking:
                backtracking = self._bad_match_logic()
            else:
                current_match_words: List[str] = self._pattern_matches[
                    self._word_index]
                current_match_word: str = current_match_words[
                    self._match_indices[self._word_index]]

                # Check word against cl_map
                current_coded_word: str = self._coded_words[self._word_index]
                # if self._is_match_good(current_coded_word,
                #                        current_match_word):
                if self.cypher_letter_map.does_word_coding_work(
                    current_coded_word, current_match_word):
                    logging.debug(
                        f"Testing word {self._word_index} == "
                        f"{current_match_word}, works")
                    self._good_match_logic(current_coded_word,
                                           current_match_word)
                else:
                    logging.debug(
                        f"Testing word {self._word_index} == "
                        f"{current_match_word}, doesn't work")
                    backtracking = self._bad_match_logic()

        if self._word_index < 0:
            logging.debug("decrypt failed")
            return False  # 6d: No decoded text could be found
        logging.debug("decrypt succeeded")
        return True  # 4c: decrypting was successful

    def _is_match_good(
        self,
        current_coded_word: str,
        current_match_word: str
    ) -> bool:
        # Select the "match word" :math:`j_x` for word :math:`i`
        current_best_decode: str = \
            self.cypher_letter_map.decode(current_coded_word)
        for letter_pair in zip(current_best_decode, current_match_word):
            decode_letter, match_letter = letter_pair
            if decode_letter == '_':
                continue
            if decode_letter != match_letter:
                return False
        return True

    def _good_match_logic(
        self,
        current_coded_word: str,
        current_match_word: str
    ):
        self.cypher_letter_map.add_word_to_mapping(current_coded_word,
                                                   current_match_word)
        self._word_index += 1

    def _bad_match_logic(
        self
    ) -> bool:
        self._match_indices[self._word_index] += 1
        match_count: int = len(self._pattern_matches[self._word_index])
        if self._match_indices[self._word_index] >= match_count:
            # a. Remove the match word from the cypher-letter map
            #         b. Set :math:`j_i` to 0
            #         c. Decrement :math:`i`
            # Repeat "bad match" steps with new :math:`i`
            #         d. If :math:`i` < 0, no decoded text can be found; return `False`.
            #         e. Otherwise, return to step 2 and repeat.
            self.cypher_letter_map.remove_last_word_from_mapping()
            self._match_indices[self._word_index] = 0
            self._word_index -= 1
            return True
        return False


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


def decrypt_quote(
    coded_quote: str,
    coded_author: str = None,
    add_words: List[str] = None,
    show_cypher: bool = False,
    rebuild_patterns: bool = False,
) -> str:
    """
    Decrypts the Cryptoquote puzzle.

    :param coded_quote: The quote portion of the puzzle. (Only this person is
      used in decoding, since names are not usually in the English dictionary.)
    :param coded_author: The author portion of the puzzle. (This will be
      decoded based on the results from decoding the quote.)
    :param add_words: Words to add to the word list before decrypting
    :param show_cypher: Whether the puzzle cypher should be added to the
      decoded puzzle text.
    :param rebuild_patterns: Whether to rebuild the saved word patterns file
      from the text corpus file
    :return: decoded puzzle text. If decoding was not successful, returns a
      blank string.
    """
    pattern_dict_file_path = os.path.join(
        os.path.dirname(__file__), PATTERNS_JSON)
    corpus_file_path = os.path.join(
        os.path.dirname(__file__), CORPUS_FILE)
    cypher_letter_map = CypherLetterMap()
    word_patterns = WordPatterns(
        pattern_dict_file_path,
        overwrite_json=rebuild_patterns,
        corpus_file_path=corpus_file_path)
    if add_words:
        word_patterns.add_new_words(add_words)
    decrypter = Decrypter(
        coded_quote,
        cypher_letter_map,
        word_patterns)
    success = decrypter.decrypt()
    logging.debug(f"{success=}")
    cypher_letter_map = decrypter.cypher_letter_map
    if success:
        decoded_quote = cypher_letter_map.decode(coded_quote)
        logging.debug(f"{decoded_quote=}")
        decoded_author = f"\n{cypher_letter_map.decode(coded_author)}" \
            if coded_author is not None \
            else ""
    else:
        decoded_quote = ""
        decoded_author = ""
    cl_map_string = f"\n{str(cypher_letter_map)}" if show_cypher else ""
    return f"{decoded_quote}{decoded_author}{cl_map_string}"


# TODO: add command line arguments to:
#       update patterns dict from corpus file
#       update corpus file from patterns dict
#       suggest words (and have them added to patterns dict if solution works)
#       force add words to patterns dict
if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    # quote: str = "Lz lv we aorbvtqr znbz we inlohqry bqr mqrr byh nbaae, " \
    #               "byh tyqrvzqblyrh ge abqryzbo zeqbyye. Osjr lv znr inbly " \
    #               "cnrqrge zs glyh b inloh zs lzv abqryzv."
    # print(decrypt_quote(quote, show_cypher=True))
    CODED_QUOTE = "JRR FSAAGFFZSR HGBHRG VGL JLM CBVGL JQG UDI MQGJVGQF. " \
                  "EKGN DVJIDLG CKJE EKGDQ ZSESQG ABSRM UG, DMGJR DL GYGQN " \
                  "QGFHGAE, JLM EKGL EKGN CBQW GYGQN MJN EBCJQM EKGDQ " \
                  "MDFEJLE YDFDBL, EKJE IBJR BQ HSQHBFG."
    DECODED_QUOTE = "ALL SUCCESSFUL PEOPLE MEN AND WOMEN ARE BIG DREAMERS. " \
                    "THEY IMAGINE WHAT THEIR FUTURE COULD BE, IDEAL IN EVERY " \
                    "RESPECT, AND THEN THEY WORK EVERY DAY TOWARD THEIR " \
                    "DISTANT VISION, THAT GOAL OR PURPOSE."
    decoded_words = string_to_caps_words(DECODED_QUOTE)
    print(decrypt_quote(CODED_QUOTE, add_words=decoded_words))
