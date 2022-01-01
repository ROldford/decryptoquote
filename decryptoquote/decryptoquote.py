# -*- coding: utf-8 -*-

"""
Main module.
"""
import os
import logging
from typing import List, Dict
import pymongo

from decryptoquote.cypherlettermap import CypherLetterMap
from decryptoquote.decrypter import Decrypter
from decryptoquote.helpers import string_to_caps_words
from decryptoquote.wordpatterns import WordPatterns

MONGO_HOST: str = os.environ.get('MONGODB_URI')
if MONGO_HOST is None:
    MONGO_HOST: str = 'localhost'
DB_NAME: str = os.environ.get('MONGODB_NAME')
if DB_NAME is None:
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
) -> List[Dict[str, str]]:
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
      or an empty list if no solution is found.
      Solutions use the following schema:

      {
        decoded_quote: [decoded quote],
        decoded_author: [decoded author, or None if no coded author given],
        coding_key: [solution's coding key]
      }
    """
    decrypter = _setup_decryption(add_words, coded_quote, rebuild_patterns)
    solution_maps = decrypter.decrypt_all()
    solutions = []
    for s_map in solution_maps:
        decoded_quote = s_map.decode(coded_quote)
        logging.debug(f"{decoded_quote=}")
        decoded_author = s_map.decode(coded_author) \
            if coded_author is not None \
            else ""
        keystring = s_map.keystring() if show_cypher else None
        solution = {
            'decoded_quote': decoded_quote,
            'decoded_author': decoded_author,
            'coding_key': keystring
        }
        solutions.append(solution)
    return solutions


def decrypt_quote(
    coded_quote: str,
    coded_author: str = None,
    add_words: List[str] = None,
    show_cypher: bool = False,
    rebuild_patterns: bool = False,
) -> List[Dict[str, str]]:
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
    :return: single element list containing the first valid solution,
      or an empty list if no solution is found.
      Solutions use the following schema:

      {
        decoded_quote: [decoded quote],
        decoded_author: [decoded author, or None if no coded author given],
        coding_key: [solution's coding key]
      }
    """
    decrypter = _setup_decryption(add_words, coded_quote, rebuild_patterns)
    success = decrypter.decrypt()
    logging.debug(f"{success=}")
    cypher_letter_map = decrypter.cypher_letter_map
    cl_map_string = cypher_letter_map.keystring() if show_cypher else None
    if success:
        decoded_quote = cypher_letter_map.decode(coded_quote)
        logging.debug(f"{decoded_quote=}")
        decoded_author = cypher_letter_map.decode(coded_author) \
            if coded_author is not None \
            else None
        solution = {
            'decoded_quote': decoded_quote,
            'decoded_author': decoded_author,
            'coding_key': cl_map_string
        }
        return [solution]
    else:
        return []


def _setup_decryption(add_words, coded_quote, rebuild_patterns):
    corpus_file_path = os.path.join(
        os.path.dirname(__file__), CORPUS_FILE)
    cypher_letter_map = CypherLetterMap()
    client = pymongo.MongoClient(MONGO_HOST)
    collection = client[DB_NAME][COLLECTION_NAME]
    if collection.estimated_document_count() == 0:
        rebuild_patterns = True
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
