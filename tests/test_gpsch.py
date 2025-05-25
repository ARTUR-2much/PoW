import pytest
from gspch import PRNG
from streebog import digest

@ pytest.fixture
def zero_prng():
    # Seed = 32-byte zero vector, replicates h0 = zeros
    seed = b"\x00" * 32
    return PRNG(seed)

@ pytest.fixture
def rnd_prng():
    # Arbitrary non-zero seed for variation
    seed = digest(b"TestSeed")
    return PRNG(seed)


def test_get_bytes_correct_hi(zero_prng):
    prng = zero_prng
    # Build input block: first 56 bytes of h0 (zeros) + counter=1 as BE64
    block = (b"\x00" * 56) + (1).to_bytes(8, byteorder="big")
    expected_hi = digest(block)
    # First get_bytes(32) should equal expected_hi
    out = prng.get_bytes(32)
    assert out == expected_hi


def test_get_bytes_boundary(zero_prng):
    prng = zero_prng
    # Prepare expected for 48 bytes: hi1 (32 bytes) + first 16 of hi2
    block1 = (b"\x00" * 56) + (1).to_bytes(8, byteorder="big")
    hi1 = digest(block1)
    block2 = (b"\x00" * 56) + (2).to_bytes(8, byteorder="big")
    hi2 = digest(block2)
    expected = hi1 + hi2[:16]
    out = prng.get_bytes(48)
    assert out == expected


def test_get_int_range(rnd_prng):
    prng = rnd_prng
    q = 1000
    # sample multiple times
    for _ in range(20):
        x = prng.get_int(q)
        assert 0 <= x < q


def test_get_nonce_range(rnd_prng):
    prng = rnd_prng
    q = 101
    k = prng.get_nonce(q)
    assert 1 <= k < q


def test_get_hex_consistency(rnd_prng):
    prng = rnd_prng
    # get_hex should match get_bytes.hex()
    n = 10
    p = PRNG(prng.h0)
    hex1 = p.get_hex(n)
    # replicate: new PRNG with same state
    p2 = PRNG(prng.h0)
    out_bytes = p2.get_bytes(n)
    assert hex1 == out_bytes.hex()


def test_reproducible_stream():
    seed = digest(b"Reproducible")
    p1 = PRNG(seed)
    p2 = PRNG(seed)
    # consuming same amounts yields identical streams
    a1 = p1.get_bytes(50)
    a2 = p2.get_bytes(50)
    assert a1 == a2
    b1 = p1.get_bytes(30)
    b2 = p2.get_bytes(30)
    assert b1 == b2
