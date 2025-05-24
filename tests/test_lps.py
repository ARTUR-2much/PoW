import pytest
from streebog import lps


def test_lps_returns_bytes_and_correct_length():
    v = bytes(range(64))
    r = lps(v)
    assert isinstance(r, bytes)
    assert len(r) == 64


def test_lps_changes_input():
    v = bytes(range(64))
    r = lps(v)
    assert r != v


def test_lps_is_deterministic():
    v = bytes(range(64))
    assert lps(v) == lps(v)
