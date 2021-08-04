#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Integration tests for `decryptoquote` package."""

import pytest

from decryptoquote import decryptoquote

@pytest.mark.xfail
class TestIntegration(object):
    CODED_QUOTE: str = "coded_quote"
    DECODED_QUOTE: str = "decoded_quote"
    test_data_noauthor = [
        {
            CODED_QUOTE: "KYHJ HJMHMQM FKNJ LZHJX YQQZJPZP QN. XNP ACHMKZTM "
                         "QN FM HJ NFT KDZYMFTZM, MKZYEM HJ NFT SNJMSHZJSZM, "
                         "LFQ MCNFQM HJ NFT KYHJM. HQ HM CHM OZXYKCNJZ QN "
                         "TNFMZ Y PZYV ANTDP.",
            DECODED_QUOTE: "PAIN INSISTS UPON BEING ATTENDED TO. GOD WHISPERS "
                           "TO US IN OUR PLEASURES, SPEAKS IN OUR "
                           "CONSCIENCES, BUT SHOUTS IN OUR PAINS. IT IS HIS "
                           "MEGAPHONE TO ROUSE A DEAF WORLD."
        },
        {
            CODED_QUOTE: "ML INH'DX SNV JEOMST FNJXNSX XZFX'F ZMLX RXVVXD, "
                         "VQXS INH'DX PEFVMST INHD VMJX. INHD ZMLX PMZZ "
                         "RXWNJX RXVVXD RI JEOMST NVQXD ZMKXF RXVVXD.",
            DECODED_QUOTE: "IF YOU'RE NOT MAKING SOMEONE ELSE'S LIFE BETTER, "
                           "THEN YOU'RE WASTING YOUR TIME. YOUR LIFE WILL "
                           "BECOME BETTER BY MAKING OTHER LIVES BETTER."
        },
        {
            CODED_QUOTE: "JRR FSAAGFFZSR HGBHRG VGL JLM CBVGL JQG UDI "
                         "MQGJVGQF. EKGN DVJIDLG CKJE EKGDQ ZSESQG ABSRM UG, "
                         "DMGJR DL GYGQN QGFHGAE, JLM EKGL EKGN CBQW GYGQN "
                         "MJN EBCJOM EKGDO MDFEJLE YDFDBL, EKJE IBJR BQ "
                         "HSQHBFG.",
            DECODED_QUOTE: "ALL SUCCESSFUL PEOPLE MEN AND WOMEN ARE BIG "
                           "DREAMERS. THEY IMAGINE WHAT THEIR FUTURE COULD "
                           "BE, IDEAL IN EVERY RESPECT, AND THEN THEY WORK "
                           "EVERY DAY TOWARD THEIR DISTANT VISION, THAT GOAL "
                           "OR PURPOSE."
        },
        {
            CODED_QUOTE: "Lz lv we aorbvtqr znbz we inlohqry bqr mqrr byh "
                         "nbaae, byh tyqrvzqblyrh ge abqryzzbo zeqbyye. Osjr "
                         "lv znr inbly cnrqrge zs glyh b inloh zs lzv "
                         "abqryzv.",
            DECODED_QUOTE: "IT IS MY PLEASURE THAT MY CHILDREN ARE FREE AND "
                           "HAPPY, AND UNRESTRAINED BY PARENTAL TYRANNY. LOVE "
                           "IS THE CHAIN WHEREBY TO BIND A CHILD TO ITS "
                           "PARENTS. "
        },
    ]

    @pytest.mark.parametrize("test_strings", test_data_noauthor)
    def test_no_author(self, test_strings):
        coded_quote: str = test_strings[self.CODED_QUOTE]
        decoded_quote: str = test_strings[self.DECODED_QUOTE]
        result = decryptoquote.decrypt_quote(coded_quote)
        assert result == decoded_quote
