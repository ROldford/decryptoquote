from typing import Dict, Optional, List, Tuple

from decryptoquote.constants import LETTERS, PUNCTUATION


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
        keystring: str = self.keystring()
        return f"Decoder:\n{LETTERS}\n{keystring}"

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

    def keystring(self):
        key: List[str] = []
        for letter in LETTERS:
            letter_for_key = self._clmap[letter]
            if letter_for_key is None:
                key.append("_")
            else:
                key.append(letter_for_key)
        return ''.join(key)

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
