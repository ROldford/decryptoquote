import logging
from typing import List

from decryptoquote.cypherlettermap import CypherLetterMap
from decryptoquote.helpers import string_to_caps_words
from decryptoquote.wordpatterns import WordPatterns


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
