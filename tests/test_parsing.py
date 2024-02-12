from diracdec import *



def test_1():
    wolfram_backend.wolfram_start()
    a = parse(''' 'ss + ss' ''')
    b = parse(''' '2 ss' ''')
    assert a == b
    assert hash(a) == hash(b)
    wolfram_backend.wolfram_terminate()
