#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for PuzzleTree class in `decryptoquote` package."""
from typing import List, Dict

import pytest

from decryptoquote.decryptoquote import Puzzle, PuzzleTree

test_string: str = "Svool, R'n z hgirmt!"
test_coded_quote_words: List[str] = ['SVOOL', ',', "R'N", 'Z', 'HGIRMT', '!']
test_author: str = "Ibzm"
test_coded_author_words: List[str] = ['IBZM']
# TODO: turn blank, etc. string literals into constants
BLANK = "blank"
# IN_PROGRESS = "in_progress"
# FINISHED = "finished"
AUTHOR = "author"
NO_AUTHOR = "no-author"
decoded_quote: Dict[str, List[str]] = {
    BLANK: ['*****', ',', "*'*", '*', '******', '!'],
    # IN_PROGRESS: ['**LL*', ',', "*'*", 'A', '**R***', '!'],
    # FINISHED: ['HELLO', ',', "I'M", 'A', 'STRING', '!']
}
decoded_author: Dict[str, List[str]] = {
    BLANK: ['****'],
    # IN_PROGRESS: ['R***'],
    # FINISHED: ['RYAN']
}
coding_dict: Dict[str, Dict[str, str]] = {
    BLANK:
        {
            "A": "*", "B": "*", "C": "*", "D": "*", "E": "*",
            "F": "*", "G": "*", "H": "*", "I": "*", "J": "*",
            "K": "*", "L": "*", "M": "*", "N": "*", "O": "*",
            "P": "*", "Q": "*", "R": "*", "S": "*", "T": "*",
            "U": "*", "V": "*", "W": "*", "X": "*", "Y": "*", "Z": "*"
        },
    # IN_PROGRESS:
    #     {
    #         "A": "Z", "B": "*", "C": "*", "D": "*", "E": "*",
    #         "F": "*", "G": "*", "H": "*", "I": "*", "J": "*",
    #         "K": "*", "L": "O", "M": "*", "N": "*", "O": "*",
    #         "P": "*", "Q": "*", "R": "I", "S": "*", "T": "*",
    #         "U": "*", "V": "*", "W": "*", "X": "*", "Y": "*", "Z": "*"
    #     },
    # FINISHED:
    #     {
    #         "A": "Z", "B": "Y", "C": "X", "D": "W", "E": "V",
    #         "F": "U", "G": "T", "H": "S", "I": "R", "J": "Q",
    #         "K": "P", "L": "O", "M": "N", "N": "M", "O": "L",
    #         "P": "K", "Q": "J", "R": "I", "S": "H", "T": "G",
    #         "U": "F", "V": "E", "W": "D", "X": "C", "Y": "B", "Z": "A"
    #     }
}


@pytest.fixture()
def puzzle_tree() -> Dict[str, PuzzleTree]:
    pt_dict: Dict[str, PuzzleTree] = {
        AUTHOR: PuzzleTree(test_string, test_author),
        NO_AUTHOR: PuzzleTree(test_string)
    }
    return pt_dict


def test_make_initial_puzzle(puzzle_tree):
    assert len(puzzle_tree[AUTHOR].worklist) == 1
    puzzle_author: Puzzle = puzzle_tree[AUTHOR].worklist[0]
    assert puzzle_author.coding_dict == coding_dict[BLANK]
    assert puzzle_author.coded_quote_words == test_coded_quote_words
    assert puzzle_author.coded_author_words == test_coded_author_words
    assert puzzle_author.decoded_quote_words == decoded_quote[BLANK]
    assert puzzle_author.decoded_author_words == decoded_author[BLANK]
    assert len(puzzle_tree[NO_AUTHOR].worklist) == 1
    puzzle_noauthor: Puzzle = puzzle_tree[NO_AUTHOR].worklist[0]
    assert puzzle_noauthor.coding_dict == coding_dict[BLANK]
    assert puzzle_noauthor.coded_quote_words == test_coded_quote_words
    assert puzzle_noauthor.decoded_quote_words == decoded_quote[BLANK]

def test_get_next_puzzle_from_worklist(puzzle_tree):
    pt_author: PuzzleTree = puzzle_tree[AUTHOR]
    first_puzzle: Puzzle = pt_author.get_next_puzzle_from_worklist()
    assert len(pt_author.worklist) == 0
    assert first_puzzle.coding_dict == coding_dict[BLANK]
    with pytest.raises(IndexError):
        not_puzzle = pt_author.get_next_puzzle_from_worklist()


@pytest.mark.xfail
def test_make_puzzles_from_matches(puzzle_tree):
    assert False

#
# @pytest.fixture()
# def puzzles():
#     puzzles_dict = {
#         AUTHOR: {
#             BLANK: decryptoquote.Puzzle(
#                 coding_dict[BLANK],
#                 test_coded_quote_words,
#                 decoded_quote[BLANK],
#                 test_coded_author_words,
#                 decoded_author[BLANK]
#             ),
#             IN_PROGRESS: decryptoquote.Puzzle(
#                 coding_dict[IN_PROGRESS],
#                 test_coded_quote_words,
#                 decoded_quote[IN_PROGRESS],
#                 test_coded_author_words,
#                 decoded_author[IN_PROGRESS]
#             ),
#             FINISHED: decryptoquote.Puzzle(
#                 coding_dict[FINISHED],
#                 test_coded_quote_words,
#                 decoded_quote[FINISHED],
#                 test_coded_author_words,
#                 decoded_author[FINISHED]
#             )
#         },
#         NO_AUTHOR: {
#             BLANK: decryptoquote.Puzzle(
#                 coding_dict[BLANK],
#                 test_coded_quote_words,
#                 decoded_quote[BLANK]
#             ),
#             IN_PROGRESS: decryptoquote.Puzzle(
#                 coding_dict[IN_PROGRESS],
#                 test_coded_quote_words,
#                 decoded_quote[IN_PROGRESS]
#             ),
#             FINISHED: decryptoquote.Puzzle(
#                 coding_dict[FINISHED],
#                 test_coded_quote_words,
#                 decoded_quote[FINISHED]
#             )
#         }
#     }
#     return puzzles_dict
#
#
# @pytest.fixture()
# def model(fs):
#     test_corpus = "Hello, I'm a string!"
#     corpus_file_path = '/test.txt'
#     fs.create_file(corpus_file_path, contents=test_corpus)
#     # TODO: remove file open
#     with open(corpus_file_path) as f:
#         model = decryptoquote.LanguageModel(corpus_file_path)
#     return decryptoquote.LanguageModel(corpus_file_path)
#
#
# def test_init_puzzle(puzzles):
#     test_puzzle = puzzles[AUTHOR][BLANK]
#     assert test_puzzle.coded_quote_words == test_coded_quote_words
#     assert test_puzzle.decoded_quote_words == decoded_quote[BLANK]
#     assert test_puzzle.coded_author_words == test_coded_author_words
#     assert test_puzzle.decoded_author_words == decoded_author[BLANK]
#     assert test_puzzle.coding_dict == coding_dict[BLANK]
#
#     test_puzzle = puzzles[NO_AUTHOR][BLANK]
#     assert test_puzzle.coded_quote_words == test_coded_quote_words
#     assert test_puzzle.decoded_quote_words == decoded_quote[BLANK]
#     assert test_puzzle.coding_dict == coding_dict[BLANK]
#
#     test_puzzle = puzzles[AUTHOR][IN_PROGRESS]
#     assert test_puzzle.coded_quote_words == test_coded_quote_words
#     assert test_puzzle.decoded_quote_words == decoded_quote[IN_PROGRESS]
#     assert test_puzzle.coded_author_words == test_coded_author_words
#     assert test_puzzle.decoded_author_words == decoded_author[IN_PROGRESS]
#     assert test_puzzle.coding_dict == coding_dict[IN_PROGRESS]
#
#     test_puzzle = puzzles[NO_AUTHOR][IN_PROGRESS]
#     assert test_puzzle.coded_quote_words == test_coded_quote_words
#     assert test_puzzle.decoded_quote_words == decoded_quote[IN_PROGRESS]
#     assert test_puzzle.coding_dict == coding_dict[IN_PROGRESS]
#
#
# def test_is_solved(puzzles):
#     assert puzzles[AUTHOR][BLANK].is_solved() is False
#     assert puzzles[AUTHOR][IN_PROGRESS].is_solved() is False
#     assert puzzles[AUTHOR][FINISHED].is_solved() is True
#     assert puzzles[NO_AUTHOR][BLANK].is_solved() is False
#     assert puzzles[NO_AUTHOR][IN_PROGRESS].is_solved() is False
#     assert puzzles[NO_AUTHOR][FINISHED].is_solved() is True
#
#
# def test_get_solution_string(puzzles):
#     assert puzzles[AUTHOR][FINISHED].get_solution_string() \
#         == "HELLO, I'M A STRING! - RYAN"
#     assert puzzles[NO_AUTHOR][FINISHED].get_solution_string() \
#         == "HELLO, I'M A STRING!"
