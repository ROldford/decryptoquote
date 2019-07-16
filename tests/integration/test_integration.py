#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Integration tests for `decryptoquote` package."""

import pytest

from decryptoquote import decryptoquote

class TestIntegration(object):
    def test_quote_1(self):
        coded_quote = """   KYHJ HJMHMQM FKNJ LZHJX YQQZJPZP QN. XNP ACHMKZTM
                            QN FM HJ NFT KDZYMFTZM, MKZYEM HJ NFT SNJMSHZJSZM,
                            LFQ MCNFQM HJ NFT KYHJM. HQ HM CHM OZXYKCNJZ QN
                            TNFMZ Y PZYV ANTDP."""
        plaintext = """     PAIN INSISTS UPON BEING ATTENDED TO. GOD WHISPERS
                            TO US IN OUR PLEASURES, SPEAKS IN OUR CONSCIENCES,
                            BUT SHOUTS IN OUR PAINS. IT IS HIS MEGAPHONE TO
                            ROUSE A DEAF WORLD."""
        result = decryptoquote.decryptQuote(coded_quote)
        assert type(result).__name__ == 'str'


    def test_quote_2(self):
        coded_quote = """   ML INH'DX SNV JEOMST FNJXNSX XZFX'F ZMLX RXVVXD,
                            VQXS INH'DX PEFVMST INHD VMJX. INHD ZMLX PMZZ
                            RXWNJX RXVVXD RI JEOMST NVQXD ZMKXF RXVVXD."""
        plaintext = """     IF YOU'RE NOT MAKING SOMEONE ELSE'S LIFE BETTER,
                            THEN YOU'RE WASTING YOUR TIME. YOUR LIFE WILL
                            BECOME BETTER BY MAKING OTHER LIVES BETTER."""
        result = decryptoquote.decryptQuote(coded_quote)
        assert type(result).__name__ == 'str'
