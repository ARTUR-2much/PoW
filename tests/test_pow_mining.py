from main_PoW import PowHeader, find_nonce, FIVE_ZERO_BITS
from main_PoW import _make_prev_hash, _timestamp_now_bytes, _make_leaves
from merkle import calc_root


def test_find_nonce_streebog():
    leaves = _make_leaves()
    root = calc_root(leaves, duplicate_last=False)
    hdr = PowHeader(
        size=len(leaves),
        prev_hash=_make_prev_hash(),
        merkle_root=root,
        timestamp=_timestamp_now_bytes(),
        nonce=0
    )
    hdr = find_nonce(hdr)
    h = hdr.hash()
    assert h[0] >> (8 - FIVE_ZERO_BITS) == 0      # 5 ведущих нулевых бит
