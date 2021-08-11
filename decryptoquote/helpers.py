import re
from typing import List


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
