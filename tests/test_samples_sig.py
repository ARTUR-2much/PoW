from pathlib import Path
from streebog import digest
from schnorr import PublicKey, PrivateKey
from gspch import PRNG

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "samples"
SEED_TXT = b"Artur Mkhitarian"


def _load_sig(sig_path: Path):
    raw = sig_path.read_bytes()
    assert len(raw) == 96
    R = int.from_bytes(raw[:64], "big")
    s = int.from_bytes(raw[64:], "big")
    return R, s

def test_all_signatures_ok():
    stored_seed = (SAMPLES / "seed.bin").read_bytes()
    assert stored_seed == digest(SEED_TXT), (
        "seed.bin не совпадает с digest(SEED_TXT) — "
        "файлы .sig сгенерированы не тем сидом"
    )


    prng = PRNG(stored_seed)
    sk = PrivateKey.generate(prng)
    pk = PublicKey(sk.y)

    for bin_path in sorted(SAMPLES.glob("sample*.bin")):
        R, s = _load_sig(bin_path.with_suffix(".sig"))
        data = bin_path.read_bytes()
        assert pk.verify(data, (R, s)), f"подпись не бьётся для {bin_path.name}"
