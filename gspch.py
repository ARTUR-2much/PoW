# prng.py
# Детерминированный генератор псевдослучайных битов на основе Стрибога-256

from streebog import digest

# gspch.py
class PRNG:
    def __init__(self, seed: bytes, *, debug: bool = True):
        assert len(seed) in (32, 64)
        self.h0 = seed.ljust(64, b"\x00")
        self.counter = 1
        self.buffer = b""

        if debug:
            print(f"[PRNG] seed = {seed!r}")
            print(f"[PRNG] h0 = {self.h0.hex()[:64]}…")


    def _refill(self):
        """
        Вычисляет следующий блок hi = digest(h0 || BE64(counter)),
        добавляет в буфер и инкрементирует счётчик.
        """
        # BE64(counter)
        be64 = self.counter.to_bytes(8, byteorder="big")
        # входной блок: h0 (64 байта) + счётчик (8 байт) => 72 байта, но digest обрежет до 64
        # Поэтому используем только первые 64 байта: h0[:56] + be64
        block = self.h0[:56] + be64
        hi = digest(block)
        self.buffer += hi
        self.counter += 1

    def get_bytes(self, n: int) -> bytes:
        """
        Возвращает n байт из потока, генерируя при необходимости новые hi.
        """
        while len(self.buffer) < n:
            self._refill()
        result = self.buffer[:n]
        self.buffer = self.buffer[n:]
        return result

    def get_int(self, q: int) -> int:
        """
        Получает целое в диапазоне [0, q) методом rejection sampling.
        """
        from math import ceil
        bits = q.bit_length()
        bytes_needed = ceil(bits / 8)
        while True:
            chunk = self.get_bytes(bytes_needed)
            x = int.from_bytes(chunk, byteorder="big")
            if x < q:
                return x

    def get_nonce(self, q: int) -> int:
        """
        Возвращает k в диапазоне [1, q-1], пригодный для одноразового ключа в схеме подписи.
        """
        # исключаем 0, поэтому диапазон 1..q-1
        return self.get_int(q - 1) + 1

    def get_hex(self, n: int) -> str:
        """
        Удобный метод: выдать n байт в виде шестнадцатеричной строки.
        """
        return self.get_bytes(n).hex()
