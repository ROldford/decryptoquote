import json
import os
from typing import Optional, Dict, List

from decryptoquote.constants import PUNCTUATION


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

    DIGITS: str = "0123456789"

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
                if character in self.DIGITS:
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
