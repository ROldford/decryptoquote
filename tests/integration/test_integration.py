#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Integration tests for `decryptoquote` package."""

import pytest

from decryptoquote import decryptoquote

@pytest.mark.xfail
class TestIntegration(object):
    test_data = [
        (
            """ KYHJ HJMHMQM FKNJ LZHJX YQQZJPZP QN. XNP ACHMKZTM
                QN FM HJ NFT KDZYMFTZM, MKZYEM HJ NFT SNJMSHZJSZM,
                LFQ MCNFQM HJ NFT KYHJM. HQ HM CHM OZXYKCNJZ QN
                TNFMZ Y PZYV ANTDP.""",
            """ PAIN INSISTS UPON BEING ATTENDED TO. GOD WHISPERS
                TO US IN OUR PLEASURES, SPEAKS IN OUR CONSCIENCES,
                BUT SHOUTS IN OUR PAINS. IT IS HIS MEGAPHONE TO
                ROUSE A DEAF WORLD."""
        ),
        (
            """ ML INH'DX SNV JEOMST FNJXNSX XZFX'F ZMLX RXVVXD,
                VQXS INH'DX PEFVMST INHD VMJX. INHD ZMLX PMZZ
                RXWNJX RXVVXD RI JEOMST NVQXD ZMKXF RXVVXD.""",
            """ IF YOU'RE NOT MAKING SOMEONE ELSE'S LIFE BETTER,
                THEN YOU'RE WASTING YOUR TIME. YOUR LIFE WILL
                BECOME BETTER BY MAKING OTHER LIVES BETTER."""
        ),
        (
            """ JRR FSAAGFFZSR HGBHRG VGL JLM CBVGL JQG UDI MQGJVGQF. EKGN DVJIDLG
                CKJE EKGDQ ZSESQG ABSRM UG, DMGJR DL GYGQN QGFHGAE, JLM EKGL EKGN
                CBQW GYGQN MJN EBCJOM EKGDO MDFEJLE YDFDBL, EKJE IBJR BQ
                HSQHBFG.""",
            """ ALL SUCCESSFUL PEOPLE MEN AND WOMEN ARE BIG DREAMERS. THEY IMAGINE
                WHAT THEIR FUTURE COULD BE, IDEAL IN EVERY RESPECT, AND THEN THEY
                WORK EVERY DAY TOWARD THEIR DISTANT VISION, THAT GOAL OR
                PURPOSE."""
        ),
    ]

    @pytest.mark.parametrize("coded_quote, decoded", test_data)
    def test_is_correct(self, coded_quote, decoded):
        result = decryptoquote.decryptQuote(coded_quote)
        assert result == decoded
