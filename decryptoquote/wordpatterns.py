from typing import TYPE_CHECKING, Optional, Dict, List, Set

from decryptoquote.constants import PUNCTUATION

if TYPE_CHECKING:
    from pymongo.collection import Collection


class WordPatterns:
    """
    This class organizes a set of English words by the pattern of distinct
    letters in each word. For example, "this" has the pattern "1.2.3.4", since
    each letter is distinct, as does "code", while "noon" has the pattern
    "1.2.2.1". Since Cryptoquotes use a substitution cypher, the coded and
    decoded words will have the same pattern. This can be used to determine
    which words are possible matches.

    :param db_collection: MongoDB collection for language model. Documents in
      this collection should follow the pattern
      ```{self.WORD_KEY: [word], self.PATTERN_KEY: [pattern]}```, with no
      duplicate words
    :param overwrite_patterns: if `True`, overwrites any existing saved patterns
      file
    :param corpus_file_path: path to language corpus file. This is required to
      make a new saved patterns file
    :exception OSError if corpus file is invalid
    """

    DIGITS: str = "0123456789"
    WORD_KEY: str = 'word'
    PATTERN_KEY: str = 'pattern'

    def __init__(self,
                 db_collection: 'Collection',
                 overwrite_patterns: bool = False,
                 corpus_file_path: Optional[str] = None) -> None:
        self._db_collection = db_collection
        self._db_collection.create_index(self.WORD_KEY, unique=True)
        self._corpus_file_path: Optional[str] = corpus_file_path
        if overwrite_patterns:
            if corpus_file_path is None:
                raise ValueError('No valid language file given')
            self._db_collection.delete_many({})

            # get words from corpus text file
            with open(corpus_file_path, 'r') as file:
                word_list: List[str] = [
                    s.upper() for s in file.read().splitlines()
                ]
                word_set: Set[str] = set(word_list)
                insert_list: List[Dict[str, str]] = []
                for word in word_set:
                    pattern: str = self.word_to_pattern(word)
                    # insert_set.add({self.WORD_KEY: word,
                    #                 self.PATTERN_KEY: pattern})
                    insert_list.append({self.WORD_KEY: word,
                                        self.PATTERN_KEY: pattern})
                x = self._db_collection.insert_many(insert_list)

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
        query = {self.PATTERN_KEY: pattern}

        query_count = self._db_collection.count_documents(query)
        if query_count < 1:
            for character in pattern:
                if character in self.DIGITS:
                    return []
            return [pattern]
        else:
            query_results = self._db_collection.find(query)
            results_list = [x[self.WORD_KEY] for x in query_results]
            return results_list

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
                self._db_collection.insert_one({self.WORD_KEY: word_upper,
                                                self.PATTERN_KEY: pattern})

    def save_corpus_from_patterns(self, corpus_file_path: str) -> None:
        pass  # TODO: stub
