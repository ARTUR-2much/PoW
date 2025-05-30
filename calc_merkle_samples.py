"""
Считает Merkle-корень для sample*.bin + sample*.sig.
root_dup  – BTC-стиль (дублирование последнего).
root_lift – выбрал вариант «поднять одиночный».
"""

from pathlib import Path
from streebog import digest
from merkle import calc_root

SAMPLES = Path("samples")


def make_leaves() -> list[bytes]:
    leaves = []
    for bin_path in sorted(SAMPLES.glob("sample*.bin")):
        sig = bin_path.with_suffix(".sig").read_bytes()
        leaves.append(digest(bin_path.read_bytes() + sig))
    return leaves


if __name__ == "__main__":
    leaves = make_leaves()
    print("Leaves:", len(leaves))

    root_dup = calc_root(leaves, duplicate_last=True)
    root_lift = calc_root(leaves, duplicate_last=False)

    print("root (duplicate last) :", root_dup.hex())
    print("root (lift single)    :", root_lift.hex())
