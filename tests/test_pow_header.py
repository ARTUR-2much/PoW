import struct
from main_PoW import PowHeader, _timestamp_now_bytes, _make_prev_hash
from streebog import digest


def test_header_serialization():
    size = 5
    prev = _make_prev_hash()
    ts = _timestamp_now_bytes()
    dummy_root = b"\x11" * 32

    hdr = PowHeader(size, prev, dummy_root, ts, nonce=0xCAFEF00D)
    b = hdr.to_bytes()
    assert len(b) == 4 + 32 + 32 + 4 + 4
    assert b[:4] == struct.pack(">I", size)
    assert b[4:36] == prev
    assert b[36:68] == dummy_root
    assert b[68:72] == ts
    assert b[-4:] == struct.pack(">I", 0xCAFEF00D)
    assert hdr.hash() == digest(b)   # Стрибог-проверка
