"""Каркас блока PoW: только заголовок и список транзакций."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from streebog import digest
from merkle import calc_root


def ts_now() -> str:
    return datetime.now().strftime("%H-%d-%m-%y")   # HH-DD-MM-YY


@dataclass
class BlockHeader:
    size: int
    prev_hash: bytes
    merkle_root: bytes
    timestamp: str
    nonce: int = 0          # майним позже

    # удобный дамп
    def pretty(self) -> str:
        return (
            f"size: {self.size}\n"
            f"prev_hash: {self.prev_hash.hex()}\n"
            f"merkle_root: {self.merkle_root.hex()}\n"
            f"timestamp: {self.timestamp}\n"
            f"nonce: {self.nonce}"
        )


class Block:
    def __init__(self, tx_paths: list[Path], prev_hash: bytes):
        self.tx_paths = tx_paths
        self.prev_hash = prev_hash

        leaves = [digest(p.read_bytes()) for p in tx_paths]
        self.merkle_root = calc_root(leaves, duplicate_last=True)

        self.header = BlockHeader(
            size=len(tx_paths),
            prev_hash=prev_hash,
            merkle_root=self.merkle_root,
            timestamp=ts_now(),
            nonce=0,
        )

    def header_bytes(self) -> bytes:
        return (
            self.header.size.to_bytes(4, "big") +
            self.header.prev_hash +
            self.header.merkle_root +
            self.header.timestamp.encode("ascii") +
            self.header.nonce.to_bytes(4, "big")
        )
