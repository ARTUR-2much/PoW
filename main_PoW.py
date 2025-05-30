import struct, time
from pathlib import Path
from streebog import digest
from merkle import calc_root
from gspch import PRNG

FIVE_ZERO_BITS = 5
SAMPLES = Path(__file__).resolve().parent / "samples"


def _make_leaves() -> list[bytes]:
    leaves = []
    for f in sorted(SAMPLES.glob("sample*.bin")):
        sig = f.with_suffix(".sig").read_bytes()
        leaves.append(digest(f.read_bytes() + sig))
    return leaves


def _timestamp_now_bytes() -> bytes:
    t = time.gmtime()
    # 4 байта: Hour, Day, Month, Year%100
    return bytes([t.tm_hour, t.tm_mday, t.tm_mon, t.tm_year % 100])


def _make_prev_hash() -> bytes:
    sec = int(time.time())
    ts4 = struct.pack(">I", sec)
    seed32 = digest(ts4)
    prng = PRNG(seed32.ljust(64, b"\x00"))
    return prng.get_bytes(32)


class PowHeader:
    __slots__ = ("size","prev_hash","merkle_root","timestamp","nonce")

    def __init__(self, size:int, prev_hash:bytes,
                 merkle_root:bytes, timestamp:bytes, nonce:int=0):
        assert len(prev_hash)==32 and len(merkle_root)==32 and len(timestamp)==4
        self.size, self.prev_hash, self.merkle_root = size, prev_hash, merkle_root
        self.timestamp, self.nonce = timestamp, nonce

    def to_bytes(self) -> bytes:
        return (
            struct.pack(">I", self.size) +
            self.prev_hash +
            self.merkle_root +
            self.timestamp +
            struct.pack(">I", self.nonce)
        )

    def hash(self) -> bytes:
        return digest(self.to_bytes())  # Streebog-256


def find_nonce(header:PowHeader, zero_bits:int=FIVE_ZERO_BITS) -> PowHeader:
    nonce = 0
    while True:
        header.nonce = nonce
        h = header.hash()
        # проверяем, что старшие zero_bits бит первого байта равны 0
        if h[0] >> (8 - zero_bits) == 0:
            return header
        nonce += 1


if __name__=="__main__":
    leaves = _make_leaves()
    merkle = calc_root(leaves, duplicate_last=False)
    hdr = PowHeader(
        size=len(leaves),
        prev_hash=_make_prev_hash(),
        merkle_root=merkle,
        timestamp=_timestamp_now_bytes()
    )
    hdr = find_nonce(hdr)
    print("nonce      =", hdr.nonce)
    print("block hash =", hdr.hash().hex())
