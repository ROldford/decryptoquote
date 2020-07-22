#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for `decryptoquote` package."""

import pytest
from decryptoquote import decryptoquote


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
