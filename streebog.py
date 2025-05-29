## streebog.py
"""ГОСТ 34.11-2018 (B-256) — константы и каркас."""

from struct import unpack
from codecs import getdecoder


_hexdecoder = getdecoder("hex")


def hexdec(data):
    """Decode hexadecimal
    """
    return _hexdecoder(data)[0]


SBOX = bytearray((
    252, 238, 221,  17, 207, 110,  49,  22, 251, 196, 250,
    218,  35, 197,   4,  77, 233, 119, 240, 219, 147,  46,
    153, 186,  23,  54, 241, 187,  20, 205,  95, 193, 249,
     24, 101,  90, 226,  92, 239,  33, 129,  28,  60,  66,
    139,   1, 142,  79,   5, 132,   2, 174, 227, 106, 143,
    160,   6,  11, 237, 152, 127, 212, 211,  31, 235,  52,
     44,  81, 234, 200,  72, 171, 242,  42, 104, 162, 253,
     58, 206, 204, 181, 112,  14,  86,   8,  12, 118,  18,
    191, 114,  19,  71, 156, 183,  93, 135,  21, 161, 150,
     41,  16, 123, 154, 199, 243, 145, 120, 111, 157, 158,
    178, 177,  50, 117,  25,  61, 255,  53, 138, 126, 109,
     84, 198, 128, 195, 189,  13,  87, 223, 245,  36, 169,
     62, 168,  67, 201, 215, 121, 214, 246, 124,  34, 185,
      3, 224,  15, 236, 222, 122, 148, 176, 188, 220, 232,
     40,  80,  78,  51,  10,  74, 167, 151,  96, 115,  30,
      0,  98,  68,  26, 184,  56, 130, 100, 159,  38,  65,
    173,  69,  70, 146,  39,  94,  85,  47, 140, 163, 165,
    125, 105, 213, 149,  59,   7,  88, 179,  64, 134, 172,
     29, 247,  48,  55, 107, 228, 136, 217, 231, 137, 225,
     27, 131,  73,  76,  63, 248, 254, 141,  83, 170, 144,
    202, 216, 133,  97,  32, 113, 103, 164,  45,  43,   9,
     91, 203, 155,  37, 208, 190, 229, 108,  82,  89, 166,
    116, 210, 230, 244, 180, 192, 209, 102, 175, 194,  57,
     75,  99, 182,
))

TAU = [
     0,  8, 16, 24, 32, 40, 48, 56,
     1,  9, 17, 25, 33, 41, 49, 57,
     2, 10, 18, 26, 34, 42, 50, 58,
     3, 11, 19, 27, 35, 43, 51, 59,
     4, 12, 20, 28, 36, 44, 52, 60,
     5, 13, 21, 29, 37, 45, 53, 61,
     6, 14, 22, 30, 38, 46, 54, 62,
     7, 15, 23, 31, 39, 47, 55, 63
]

A = [unpack(">Q", hexdec(s))[0] for s in (
    "8e20faa72ba0b470", "47107ddd9b505a38", "ad08b0e0c3282d1c", "d8045870ef14980e",
    "6c022c38f90a4c07", "3601161cf205268d", "1b8e0b0e798c13c8", "83478b07b2468764",
    "a011d380818e8f40", "5086e740ce47c920", "2843fd2067adea10", "14aff010bdd87508",
    "0ad97808d06cb404", "05e23c0468365a02", "8c711e02341b2d01", "46b60f011a83988e",
    "90dab52a387ae76f", "486dd4151c3dfdb9", "24b86a840e90f0d2", "125c354207487869",
    "092e94218d243cba", "8a174a9ec8121e5d", "4585254f64090fa0", "accc9ca9328a8950",
    "9d4df05d5f661451", "c0a878a0a1330aa6", "60543c50de970553", "302a1e286fc58ca7",
    "18150f14b9ec46dd", "0c84890ad27623e0", "0642ca05693b9f70", "0321658cba93c138",
    "86275df09ce8aaa8", "439da0784e745554", "afc0503c273aa42a", "d960281e9d1d5215",
    "e230140fc0802984", "71180a8960409a42", "b60c05ca30204d21", "5b068c651810a89e",
    "456c34887a3805b9", "ac361a443d1c8cd2", "561b0d22900e4669", "2b838811480723ba",
    "9bcf4486248d9f5d", "c3e9224312c8c1a0", "effa11af0964ee50", "f97d86d98a327728",
    "e4fa2054a80b329c", "727d102a548b194e", "39b008152acb8227", "9258048415eb419d",
    "492c024284fbaec0", "aa16012142f35760", "550b8e9e21f7a530", "a48b474f9ef5dc18",
    "70a6a56e2440598e", "3853dc371220a247", "1ca76e95091051ad", "0edd37c48a08a6d8",
    "07e095624504536c", "8d70c431ac02a736", "c83862965601dd1b", "641c314b2b8ee083",
)]



C = [hexdec("".join(s)) for s in (
    (
        "b1085bda1ecadae9ebcb2f81c0657c1f",
        "2f6a76432e45d016714eb88d7585c4fc",
        "4b7ce09192676901a2422a08a460d315",
        "05767436cc744d23dd806559f2a64507",
    ),
    (
        "6fa3b58aa99d2f1a4fe39d460f70b5d7",
        "f3feea720a232b9861d55e0f16b50131",
        "9ab5176b12d699585cb561c2db0aa7ca",
        "55dda21bd7cbcd56e679047021b19bb7",
    ),
    (
        "f574dcac2bce2fc70a39fc286a3d8435",
        "06f15e5f529c1f8bf2ea7514b1297b7b",
        "d3e20fe490359eb1c1c93a376062db09",
        "c2b6f443867adb31991e96f50aba0ab2",
    ),
    (
        "ef1fdfb3e81566d2f948e1a05d71e4dd",
        "488e857e335c3c7d9d721cad685e353f",
        "a9d72c82ed03d675d8b71333935203be",
        "3453eaa193e837f1220cbebc84e3d12e",
    ),
    (
        "4bea6bacad4747999a3f410c6ca92363",
        "7f151c1f1686104a359e35d7800fffbd",
        "bfcd1747253af5a3dfff00b723271a16",
        "7a56a27ea9ea63f5601758fd7c6cfe57",
    ),
    (
        "ae4faeae1d3ad3d96fa4c33b7a3039c0",
        "2d66c4f95142a46c187f9ab49af08ec6",
        "cffaa6b71c9ab7b40af21f66c2bec6b6",
        "bf71c57236904f35fa68407a46647d6e",
    ),
    (
        "f4c70e16eeaac5ec51ac86febf240954",
        "399ec6c7e6bf87c9d3473e33197a93c9",
        "0992abc52d822c3706476983284a0504",
        "3517454ca23c4af38886564d3a14d493",
    ),
    (
        "9b1f5b424d93c9a703e7aa020c6e4141",
        "4eb7f8719c36de1e89b4443b4ddbc49a",
        "f4892bcb929b069069d18d2bd1a5c42f",
        "36acc2355951a8d9a47f0dd4bf02e71e",
    ),
    (
        "378f5a541631229b944c9ad8ec165fde",
        "3a7d3a1b258942243cd955b7e00d0984",
        "800a440bdbb2ceb17b2b8a9aa6079c54",
        "0e38dc92cb1f2a607261445183235adb",
    ),
    (
        "abbedea680056f52382ae548b2e4f3f3",
        "8941e71cff8a78db1fffe18a1b336103",
        "9fe76702af69334b7a1e6c303b7652f4",
        "3698fad1153bb6c374b4c7fb98459ced",
    ),
    (
        "7bcd9ed0efc889fb3002c6cd635afe94",
        "d8fa6bbbebab07612001802114846679",
        "8a1d71efea48b9caefbacd1d7d476e98",
        "dea2594ac06fd85d6bcaa4cd81f32d1b",
    ),
    (
        "378ee767f11631bad21380b00449b17a",
        "cda43c32bcdf1d77f82012d430219f9b",
        "5d80ef9d1891cc86e71da4aa88e12852",
        "faf417d5d9b21b9948bc924af11bd720",
    ),
)]


def xor512(k: bytes, a: bytes) -> bytes:
    """
    X[k](a) = k XOR a. 6(3) в ГОСТе

    Оба аргумента должны быть ровно 64 байта (512 бит).
    Возвращает новый 64-байтовый объект.
    """
    assert len(k) == 64 and len(a) == 64, "Оба вектора должны быть 64 байта"
    return bytes(x ^ y for x, y in zip(k, a))


def sub_bytes(a: bytes) -> bytes:
    """
    S(a): нелинейное преобразование с помощью SBOX. 6(4) в ГОСТе

    Аргументы:
        a (bytes): 64-байтный входной вектор.
    Возвращает:
        bytes: 64-байтный выходной вектор, где
               каждый байт ai заменён на SBOX[ai].
    """
    # Проверяем длину
    assert len(a) == 64, f"S-преобразование ожидает 64 байта, получено {len(a)}"
    # Заменяем каждый байт через таблицу
    return bytes(SBOX[b] for b in a)


def permute(a: bytes) -> bytes:
    """
    P(a): перестановка байтов по таблице TAU. 6(5) в ГОСТе

    Аргумент:
        a (bytes): 64-байтный вход.
    Возвращает:
        bytes: 64-байтный выход, где
               result[i] = a[TAU[i]].
    """
    assert len(a) == 64, f"P-преобразование ожидает 64 байта, получено {len(a)}"
    return bytes(a[TAU[i]] for i in range(64))


def linear(a: bytes) -> bytes:
    """
    L(a): линейное преобразование 512-битного вектора a (64 байта).
    Каждый из 8 блоков по 8 байт обрабатывается как
    little-endian 64-битное слово через матрицу, заданную константами A[0..63].
    """
    assert len(a) == 64, f"L ожидает 64 байта, получено {len(a)}"
    out = bytearray(64)
    # идём по каждому из 8 слов длины 8 байт
    for word_idx in range(8):
        # извлекаем 8 байт и превращаем в число little-endian
        chunk = a[word_idx*8:(word_idx+1)*8]
        v = int.from_bytes(chunk, "little")
        acc = 0
        # для каждого бита j проверяем его значение в v
        for j in range(64):
            if (v >> j) & 1:
                acc ^= A[j]
        # результат упаковываем обратно в 8 байт little-endian
        out[word_idx*8:(word_idx+1)*8] = acc.to_bytes(8, "little")
    return bytes(out)



def lps(a: bytes) -> bytes:
    """
    Комбинированное преобразование LPS:
      1) S(a) — подстановка через SBOX
      2) P(a) — перестановка байтов по TAU
      3) L(a) — линейное смешивание с матрицей A
    Вход и выход: ровно 64 байта.
    """
    assert len(a) == 64
    b = bytes(SBOX[x] for x in a)
    c = bytes(b[TAU[i]] for i in range(64))
    out = bytearray(64)
    for col in range(8):
        chunk = c[col*8:(col+1)*8]
        bits = int.from_bytes(chunk, "little")
        acc = 0
        for i in range(64):
            if (bits >> i) & 1:
                acc ^= A[i]      # здесь A — список из 64 констант
        out[col*8:(col+1)*8] = acc.to_bytes(8, "little")
    return bytes(out)


def g(N: bytes, h: bytes, m: bytes) -> bytes:
    """
    Компрессия g(N, h, m) → новое состояние h (512 бит). - 7(8) в ГОСТе

    N, h, m — по 64 байта.
    Формулы:
      k = LPS(h XOR N)
      t = LPS(k   XOR m)
      h' = t XOR h XOR m
    """
    assert len(N) == len(h) == len(m) == 64
    k = xor512(h, N)
    k = lps(k)
    t = xor512(k, m)
    t = lps(t)
    return xor512(xor512(t, h), m)


def E(K: bytes, m: bytes) -> bytes:
    """
    Внутренний шифр E(K, m):
      — K, m: два 64-байтовых вектора.
      — Выполняет 13 раундов LPS:
        1) state = LPS(K ⊕ m)
        2) для каждой из 12 констант C[0]…C[11]:
             ключ = LPS(ключ_prev ⊕ Ci)
             state = LPS(ключ ⊕ state_prev)
      — Возвращает итоговый state (после 13-го LPS).
    """
    assert len(K) == len(m) == 64, "E: оба аргумента должны быть по 64 байта"
    # раунд 1
    key = K
    state = lps(xor512(key, m))
    # раунды 2–13
    for Ci in C:
        key = lps(xor512(key, Ci))
        state = lps(xor512(key, state))
    return state


def int_to_vec512(n: int) -> bytes:
    """
    Переводит целое число в 512-битный (64-байтный) little-endian вектор.
    Используется для подсчёта N и S.
    """
    return n.to_bytes(64, byteorder="little")


def digest(M: bytes) -> bytes:
    # Этап 1
    h = b"\x01" * 64     # IV
    N = b"\x00" * 64
    S = b"\x00" * 64

    # Этап 2
    while len(M) * 8 >= 512:
        m = M[:64]
        M = M[64:]
        h = g(N, h, m)
        N = xor512(N, int_to_vec512(512))
        S = xor512(S, m)

    # Этап 3
    r = len(M) * 8      # оставшиеся биты
    # формируем последний блок m
    m = M + b"\x01" + b"\x00" * ((64 - ((len(M)+1) % 64)) % 64)
    # сжатие
    h = g(N, h, m)
    N = xor512(N, int_to_vec512(r))
    S = xor512(S, m)
    h = g(b"\x00"*64, h, N)
    h = g(b"\x00"*64, h, S)

    # возвращаем MSB256(h)
    return h[-32:]  # или h[-32:], в зависимости от порядка байт

# ================== Self-test (optional) ==================

if __name__ == "__main__":
    vectors = {
        b"abc": "ba8063926dda4c39a51c385d8e912b7ff8d1bfbf73cce9e6f8bab3fdb4c5bb7d"[::-1],
        b"a" * 1_000_000: "6e0c9da2cb63251a65df307c36cd79ecfbc0a3e5cf1f1f4c173acbdeda8aee88",
        b"": "3f8c8e1f6a6f8e1ab2e6a1974ad4e5de571f2b319c1d3e3bf5e94a4dc04e3e2b",
    }
    print("=== Self-test: Known vectors ===")
    for msg, exp in vectors.items():
        out = digest(msg).hex()
        print(f"{msg[:10]!r}... -> {out}")
        assert out == exp, f"FAIL: got {out}, expected {exp}"
    print("All known-vector tests passed!\n")

    # 2) Avalanche test (меняем 1ый бит пустого блока)
    print("=== Self-test: Avalanche on 64-zero block ===")
    base = b"\x00" * 64
    h0 = digest(base)
    # flip первый бит
    flipped = bytes([base[0] ^ 0x01]) + base[1:]
    h1 = digest(flipped)
    # считаем Hamming distance
    dist = sum(bin(b0 ^ b1).count("1") for b0, b1 in zip(h0, h1))
    print(f"Hamming distance = {dist} bits")
    assert dist >= 128, "Avalanche test failed: too few changed bits"
    print("Avalanche property holds!\n")

    print("=== All self-tests passed. Ready to hash! ===")