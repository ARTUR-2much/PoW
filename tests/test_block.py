from pathlib import Path
from block import Block
from merkle import calc_root
from streebog import digest

SAMPLES = Path(__file__).resolve().parent.parent / "samples"


def test_block_merkle_root():
    tx_files = sorted(SAMPLES.glob("sample*.bin"))
    prev_hash = b"\x00" * 32

    block = Block(tx_files, prev_hash)

    manual = calc_root([digest(f.read_bytes()) for f in tx_files])
    assert block.header.merkle_root == manual
    assert block.header.size == 5
