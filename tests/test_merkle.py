from merkle import calc_root
from streebog import digest


def test_one_leaf_is_root():
    leaf = digest(b"abc")
    assert calc_root([leaf]) == leaf


def test_dup_vs_lift_differs():
    a, b, c = digest(b"a"), digest(b"b"), digest(b"c")
    dup = calc_root([a, b, c], duplicate_last=True)
    lift = calc_root([a, b, c], duplicate_last=False)
    assert dup != lift


def test_btc_style_known():
    # маленький ручной пример: два листа
    a, b = digest(b"a"), digest(b"b")
    root = calc_root([a, b])
    assert root == digest(a + b)
