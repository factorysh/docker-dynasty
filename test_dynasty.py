import dynasty


def test_num():
    assert dynasty.num(0) == [0]
    assert dynasty.num(1) == [1]
    assert dynasty.num(26) == [0, 1]
    assert dynasty.num(53) == [1, 2]


def test_encode():
    assert dynasty.encode(0) == "a__"
    assert dynasty.encode(25) == "z__"
    assert dynasty.encode(26) == "ab_"
    assert dynasty.encode(53) == "bc_"
