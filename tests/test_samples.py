from pathlib import Path
from gspch import PRNG  # ваш генератор
from streebog import digest  # H()
import os, sys, subprocess

# --- фикстуры -------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent  # pow_lab/


def _make_prng(seed_txt: bytes) -> PRNG:
    """Упрощённый помощник: h0 = H(seed_txt),  H(h0‖i) → поток"""
    h0 = digest(seed_txt)
    return PRNG(h0)


# --- тест 1: повторяемость ------------------------------------
def test_stream_repeatable():
    '''подтверждает детерминированность'''
    pr1 = _make_prng(b"Ivanov Ivan")
    pr2 = _make_prng(b"Ivanov Ivan")

    s1 = pr1.get_bytes(600)  # сразу 3×200
    s2 = pr2.get_bytes(600)

    assert s1 == s2  # поток детерминирован


# --- тест 2: без overlap  -------------------------------------
def test_no_overlap_early_bits():
    '''проверка на уникальноть всех разбившихся блоков'''
    pr = _make_prng(b"RandomSeed")
    first_kb = pr.get_bytes(1024)
    blocks = {first_kb[i:i + 16] for i in range(0, 1024, 16)}
    assert len(blocks) == 64

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "make_samples.py"

def test_make_samples_creates_files(tmp_path):
    assert SCRIPT.exists(), "make_samples.py не найден рядом с streebog.py"

    test_script = tmp_path / "make_samples.py"
    test_script.write_bytes(SCRIPT.read_bytes())

    # запускаем
    run = subprocess.run(
        [sys.executable, str(test_script)],
        cwd=tmp_path,
        capture_output=True, text=True
    )
    assert run.returncode == 0, f"скрипт упал: {run.stderr}"

    # ожидаем ./samples/sample1.bin…sample5.bin по 200 байт
    samples_dir = tmp_path / "samples"
    for i in range(1, 6):
        f = samples_dir / f"sample{i}.bin"
        assert f.exists(), f"{f} не создан"
        assert f.stat().st_size == 200, f"{f} не 200 байт"
