# make_samples.py
import os
from streebog import digest
from gspch import PRNG
import binascii


FIO = "heheywassapy"
seed = digest(FIO.encode("utf-8"))
prng = PRNG(seed)

OUTDIR = os.path.join(os.path.dirname(__file__), "samples")
os.makedirs(OUTDIR, exist_ok=True)

for i in range(1, 6):
    data = prng.get_bytes(200)
    if i == 1:

        pos = 50
        fio_bytes = FIO.encode("utf-8")
        data = data[:pos] + fio_bytes + data[pos+len(fio_bytes):]
    path = os.path.join(OUTDIR, f"sample{i}.bin")
    with open(path, "wb") as f:
        f.write(data)
    print(f"Saved {path}")


# for hex-dumps
hex_dump = binascii.hexlify(data).decode()
print(f"--- sample{i}.bin (hex) ---\n{hex_dump}\n")
