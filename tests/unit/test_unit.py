#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for `decryptoquote` package."""

import pytest
from decryptoquote import decryptoquote


def test_decrypt_quote():
    coded_quote: str = "Lz lv we aorbvtqr znbz we inlohqry bqr mqrr byh " \
                       "nbaae, byh tyqrvzqblyrh ge abqryzzbo zeqbyye. Osjr " \
                       "lv znr inbly cnrqrge zs glyh b inloh zs lzv abqryzv."
    coded_author: str = "Bgqbnbw Olyisoy"
    author_result: str = decryptoquote.decrypt_quote(coded_quote, coded_author)
    no_author_result: str = decryptoquote.decrypt_quote(coded_quote)
    assert author_result == "IT IS MY PLEASURE THAT MY CHILDREN ARE FREE AND " \
                            "HAPPY, AND UNRESTRAINED BY PARENTAL TYRANNY. " \
                            "LOVE IS THE CHAIN WHEREBY TO BIND A CHILD TO " \
                            "ITS PARENTS. - ABRAHAM LINCOLN "
    assert no_author_result == "IT IS MY PLEASURE THAT MY CHILDREN ARE FREE " \
                               "AND HAPPY, AND UNRESTRAINED BY PARENTAL " \
                               "TYRANNY. LOVE IS THE CHAIN WHEREBY TO BIND A " \
                               "CHILD TO ITS PARENTS."
