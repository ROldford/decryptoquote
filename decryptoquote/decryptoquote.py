# -*- coding: utf-8 -*-

"""
Main module.
"""
import os
import logging
from typing import List
import pymongo

from decryptoquote.cypherlettermap import CypherLetterMap
from decryptoquote.decrypter import Decrypter
from decryptoquote.helpers import string_to_caps_words
from decryptoquote.wordpatterns import WordPatterns

MONGO_HOST: str = 'localhost'  # TODO figure this out (env. variables?)
MONGO_PORT: int = 27017
DB_NAME: str = 'decryptoquote'
COLLECTION_NAME: str = 'wordpatterns'
CORPUS_FILE: str = "words_alpha_apos.txt"

logging.basicConfig(
    filename='decryptoquote.log',
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)


def decrypt_quote_fully(
    coded_quote: str,
    coded_author: str = None,
    add_words: List[str] = None,
    show_cypher: bool = False,
    rebuild_patterns: bool = False,
) -> List[str]:
    """
    Decrypts the Cryptoquote puzzle, finding all valid solutions.

    :param coded_quote: The quote portion of the puzzle. (Only this person is
      used in decoding, since names are not usually in the English dictionary.)
    :param coded_author: The author portion of the puzzle. (This will be
      decoded based on the results from decoding the quote.)
    :param add_words: Words to add to the word list before decrypting
    :param show_cypher: Whether the puzzle cypher should be added to the
      decoded puzzle text.
    :param rebuild_patterns: Whether to rebuild the saved word patterns file
      from the text corpus file
    :return: list of all valid puzzle solutions,
      or a blank list if no solutions could be found
    """
    decrypter = _setup_decryption(add_words, coded_quote, rebuild_patterns)
    solution_maps = decrypter.decrypt_all()
    solutions = []
    for s_map in solution_maps:
        decoded_quote = s_map.decode(coded_quote)
        logging.debug(f"{decoded_quote=}")
        decoded_author = f"\n{s_map.decode(coded_author)}" \
            if coded_author is not None \
            else ""
        cl_map_string = f"\n{str(s_map)}" if show_cypher else ""
        solutions.append(f"{decoded_quote}{decoded_author}{cl_map_string}")
    return solutions


def decrypt_quote(
    coded_quote: str,
    coded_author: str = None,
    add_words: List[str] = None,
    show_cypher: bool = False,
    rebuild_patterns: bool = False,
) -> str:
    """
    Decrypts the Cryptoquote puzzle, stopping at the first valid solution.

    :param coded_quote: The quote portion of the puzzle. (Only this person is
      used in decoding, since names are not usually in the English dictionary.)
    :param coded_author: The author portion of the puzzle. (This will be
      decoded based on the results from decoding the quote.)
    :param add_words: Words to add to the word list before decrypting
    :param show_cypher: Whether the puzzle cypher should be added to the
      decoded puzzle text.
    :param rebuild_patterns: Whether to rebuild the saved word patterns file
      from the text corpus file
    :return: decoded puzzle text. If decoding was not successful,
      returns a blank string.
    """
    decrypter = _setup_decryption(add_words, coded_quote, rebuild_patterns)
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


def _setup_decryption(add_words, coded_quote, rebuild_patterns):
    corpus_file_path = os.path.join(
        os.path.dirname(__file__), CORPUS_FILE)
    cypher_letter_map = CypherLetterMap()
    client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
    collection = client[DB_NAME][COLLECTION_NAME]
    word_patterns = WordPatterns(
        collection,
        overwrite_patterns=rebuild_patterns,
        corpus_file_path=corpus_file_path)
    if add_words:
        word_patterns.add_new_words(add_words)
    decrypter = Decrypter(
        coded_quote,
        cypher_letter_map,
        word_patterns)
    return decrypter


# TODO: add command line arguments to:
#       update patterns dict from corpus file
#       update corpus file from patterns dict
#       suggest words (and have them added to patterns dict if solution works)
#       force add words to patterns dict
if __name__ == "__main__":
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
