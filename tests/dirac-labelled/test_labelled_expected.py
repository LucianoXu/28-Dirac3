
from diracdec import *

from diracdec import parse, dirac_bigop_delta_trs as trs, label_trs

trs = trs + label_trs

def test_EXPECTED_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (A ADD B) MLTOL C ''')
        b = parse(r''' (A MLTOL C) ADD (B MLTOL C)''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_EXPECTED_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' C MLTOL (A ADD B)''')
        b = parse(r''' (C MLTOL A) ADD (C MLTOL B)''')
        assert label_trs.normalize(a) == label_trs.normalize(b)