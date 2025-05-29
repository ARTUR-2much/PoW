#!/usr/bin/env python
"""
sign_samples.py
    Подписывает все sample*.bin в ./samples/
      → sample1.sig, … sample5.sig
Формат .sig:   64-байтный R  ||  32-байтный s
"""
from pathlib import Path
from streebog import digest
from gspch import PRNG
from schnorr import PrivateKey, PublicKey

SEED_TXT = b"Artur Mkhitarian"
SAMPLES = Path("samples")
OUT_DIR = SAMPLES


prng = PRNG(digest(SEED_TXT), debug=True)
sk = PrivateKey.generate(prng)
pk = PublicKey(sk.y)

DIGEST_PATH = SAMPLES / "seed.bin"
DIGEST_PATH.write_bytes(digest(SEED_TXT))
print("Public key y =", hex(pk.y))


for bin_path in sorted(SAMPLES.glob("sample*.bin")):
    data = bin_path.read_bytes()
    R, s = sk.sign(data)

    sig_bytes = (
        R.to_bytes(64, "big") +
        s.to_bytes(32, "big")
    )
    out = OUT_DIR / (bin_path.stem + ".sig")
    out.write_bytes(sig_bytes)
    print(f"{bin_path.name:15} → {out.name}")

print("✓ 5 файлов подписаны")
