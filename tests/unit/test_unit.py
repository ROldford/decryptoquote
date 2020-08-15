#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for `decryptoquote` package."""

import pytest
# from decryptoquote import decryptoquote


# def test_decrypt_with_map():
#     # map1: Dict[str, Optional[List[str]]] = {
#     #     'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
#     #     'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
#     #     'K': ["P"], 'L': ["O"], 'M': ["N"], 'N': ["M"], 'O': ["L"],
#     #     'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
#     #     'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
#     # }
#     map1: decryptoquote.CypherLetterMap = decryptoquote.CypherLetterMap()
#     map1.add_letters_to_mapping("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
#                                 "ZYXWVUTSRQPONMLKJIHGFEDCBA")
#     # map2: Dict[str, Optional[List[str]]] = {
#     #     'A': ["Z"], 'B': ["Y"], 'C': ["X"], 'D': ["W"], 'E': ["V"],
#     #     'F': ["U"], 'G': ["T"], 'H': ["S"], 'I': ["R"], 'J': ["Q"],
#     #     'K': ["P"], 'L': ["M", "N"], 'M': ["L", "N"], 'N': ["L", "M"],
#     #     'O': ["L"],
#     #     'P': ["K"], 'Q': ["J"], 'R': ["I"], 'S': ["H"], 'T': ["G"],
#     #     'U': ["F"], 'V': ["E"], 'W': ["D"], 'X': ["C"], 'Y': ["B"], 'Z': ["A"],
#     # }
#     map2: decryptoquote.CypherLetterMap = decryptoquote.CypherLetterMap()
#     map2.add_letters_to_mapping("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
#                                 "ZYXWVUTSRQPMLLLKJIHGFEDCBA")
#     map2.add_letters_to_mapping("LMN", "NNM")
#     # map3: Dict[str, Optional[List[str]]] = {
#     #     'A': ["Z"], 'B': None, 'C': None, 'D': None, 'E': None,
#     #     'F': None, 'G': None, 'H': None, 'I': None, 'J': None,
#     #     'K': None, 'L': None, 'M': None, 'N': None, 'O': None,
#     #     'P': None, 'Q': None, 'R': None, 'S': None, 'T': None,
#     #     'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': ["A"],
#     # }
#     map3: decryptoquote.CypherLetterMap = decryptoquote.CypherLetterMap()
#     map3.add_letters_to_mapping("AZ", "ZA")
#     expected1: str = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
#     expected2: str = "ZYXWVUTSRQP___LKJIHGFEDCBA"
#     expected3: str = "Z________________________A"
#     assert decryptoquote.decrypt_with_cypherletter_map(decryptoquote.LETTERS,
#                                                        map1) == expected1
#     assert decryptoquote.decrypt_with_cypherletter_map(decryptoquote.LETTERS,
#                                                        map2) == expected2
#     assert decryptoquote.decrypt_with_cypherletter_map(decryptoquote.LETTERS,
#                                                        map3) == expected3


# def test_decrypt_quote():
#     # coded_quote: str = "Lz lv we aorbvtqr znbz we inlohqry bqr mqrr byh " \
#     #                    "nbaae, byh tyqrvzqblyrh ge abqryzzbo zeqbyye. Osjr " \
#     #                    "lv znr inbly cnrqrge zs glyh b inloh zs lzv abqryzv."
#     # coded_author: str = "Bgqbnbw Olyisoy"
#     coded_quote: str = "OIVD DIM SMQSAM OVKD XH PMGF HXLSAM. DIMF OVKD VK " \
#                        "VLMGXBV VH ZQQC VH XDH SGQLXHM."
#     coded_author: str = "TVGTVGV YQGCVK"
#     author_result: str = decryptoquote.decrypt_quote(coded_quote, coded_author)
#     no_author_result: str = decryptoquote.decrypt_quote(coded_quote)
#     assert no_author_result == "WHAT THE PEOPLE WANT IS VERY SIMPLE.  THEY WANT " \
#                                "AN AMERICA AS GOOD AS ITS PROMISE."
#     assert author_result == no_author_result + " - BARBARA JORDAN"
#     # assert no_author_result == "IT IS MY PLEASURE THAT MY CHILDREN ARE FREE " \
#     #                            "AND HAPPY, AND UNRESTRAINED BY PARENTAL " \
#     #                            "TYRANNY. LOVE IS THE CHAIN WHEREBY TO BIND A " \
#     #                            "CHILD TO ITS PARENTS."
#     # assert author_result == "IT IS MY PLEASURE THAT MY CHILDREN ARE FREE AND " \
#     #                         "HAPPY, AND UNRESTRAINED BY PARENTAL TYRANNY. " \
#     #                         "LOVE IS THE CHAIN WHEREBY TO BIND A CHILD TO " \
#     #                         "ITS PARENTS. - ABRAHAM LINCOLN "
