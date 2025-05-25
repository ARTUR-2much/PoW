from streebog import sub_bytes, SBOX # for S function
from streebog import permute, TAU # for P function
import pytest
from streebog import linear, A # for L function
from streebog import lps # for LSP-function test
from streebog import lps, sub_bytes, permute, linear # for LSP-function test as well
from streebog import E, lps # for E test



'''----------------------------S function tests------------------------------'''
def test_sub_bytes_zero():
    out = sub_bytes(b"\x00"*64)
    assert out == bytes([SBOX[0]]) * 64

def test_sub_bytes_repeat_values():
    for i in (0, 1, 2, 10, 127, 255):
        data = bytes([i]) * 64
        out = sub_bytes(data)
        assert all(b == SBOX[i] for b in out)

def test_sub_bytes_sequence():
    data = bytes(range(64))
    out  = sub_bytes(data)
    for j in range(64):
        assert out[j] == SBOX[j]

def test_antonio_grind():
    out = sub_bytes(b"\x08"*64)
    assert out == bytes([251])*64

# Проверяем первые четыре значения из таблицы π
def test_sbox_first_entries():
    data = bytes([0, 1, 2, 3] + [0]*60)  # всего 64 байта
    out  = sub_bytes(data)
    assert out[0] == 252  # π(0)=252
    assert out[1] == 238  # π(1)=238
    assert out[2] == 221  # π(2)=221
    assert out[3] ==  17  # π(3)=17

# Проверяем последнее значение
def test_sbox_last_entry():
    data = bytes([255] * 64)
    out  = sub_bytes(data)
    assert out[0] == 182  # π(255)=182

'''--------------------------------------------------------------------------'''

'''-----------------------P function tests-----------------------------------'''

def test_permute_identity_at_0():
    # Берём вектор 0..63
    data = bytes(range(64))
    out  = permute(data)
    # Проверяем, что out[0] = data[TAU[0]] = data[0]
    assert out[0] == data[TAU[0]] == 0

def test_permute_some_positions():
    data = bytes(range(64))
    out  = permute(data)
    # Проверяем пару контрольных позиций
    assert out[1] == data[TAU[1]] == 8
    assert out[10] == data[TAU[10]] == data[17]  # TAU[10]==18
    assert out[63] == data[TAU[63]]  # последний элемент перемещения
    assert out[63] == data[TAU[63]]


def test_permute_by_formula():
    data = bytes(range(64))
    out  = permute(data)
    # Проверяем формулу P(a)[i] = a[(i%8)*8 + i//8] для каждого i
    for i in range(64):
        expected = data[(i % 8) * 8 + (i // 8)]
        assert out[i] == expected, f"permute failed at i={i}: got {out[i]}, expected {expected}"


def test_permute_is_bijection():
    data = bytes(range(64))
    out  = permute(data)
    assert set(out) == set(data)
    assert len(out) == 64

'''-------------------------------------------------------------------------'''


'''---------------------L-преобразование-------------------------------------'''

def make_bit_vector(bit_index: int) -> bytes:
    """
    Создаёт 64-байтный вектор, где установлен только бит bit_index (0..511),
    в little-endian внутри каждого 8-байтного слова.
    """
    v = bytearray(64)
    # слово (0..7), внутри слова байт и бит
    word = bit_index // 64       # какой из 8 слов
    bit_in_word = bit_index % 64
    byte_in_word = bit_in_word // 8
    bit_in_byte  = bit_in_word % 8
    # global byte index
    idx = word*8 + byte_in_word
    v[idx] = 1 << bit_in_byte
    return bytes(v)

@pytest.mark.parametrize("j", [0, 63])
def test_linear_single_bit(j):
    """
    Проверяем, что L(v) для вектора с одним битом j дает A[j].
    """
    v = make_bit_vector(j)
    out = linear(v)
    # берём первые 8 байт — это результат для слова 0
    got = int.from_bytes(out[0:8], "little")
    assert got == A[j], f"linear failed for bit {j}: got A={hex(got)}, expected {hex(A[j])}"



def test_sp_zero_vector():
    # S(0^64) -> FC^64, P ничего не меняет
    sp = permute(sub_bytes(b"\x00" * 64))
    assert sp == bytes([0xFC]) * 64, f"SP(0) mismatch: got {sp.hex()}"

def test_sp_iv_vector():
    # S(01^64) -> EE^64, P ничего не меняет
    iv = b"\x01" * 64
    sp = permute(sub_bytes(iv))
    assert sp == bytes([0xEE]) * 64, f"SP(IV) mismatch: got {sp.hex()}"

'''--------------------------------------------------------------------------'''

'''----------------------------LPS-function testtt---------------------------'''

# def test_lps_zero_vector_ref():
#     # RFC 6986 §10.1.1: LPS(0^512) == b383fc2e... repeated 4×
#     expected = bytes.fromhex(
#         "b383fc2eced4a574"  # 8 байт
#         "b383fc2eced4a574"  # повторяем 4 раза
#     ) * 4
#     got = lps(b"\x00" * 64)
#     assert got == expected, f"\nLPS(0^512) mismatch:\n got:      {got.hex()}\n expected: {expected.hex()}"
#
# def test_lps_iv_vector_ref():
#     # RFC 6986 §10.1.2: LPS((0x01)^64) == 23c5ee40b07b5f15... repeated 4×
#     expected = bytes.fromhex(
#         "23c5ee40b07b5f15"
#     ) * 8  # 8×8 байт = 64 байта
#     got = lps(b"\x01" * 64)
#     assert got == expected, f"\nLPS(IV) mismatch:\n got:      {got.hex()}\n expected: {expected.hex()}"
#
# def test_lps_vs_components():
#     # фиксированный вектор, но мог быть любым
#     a = bytes(range(64))
#     # lps(a) должно совпадать с L(P(S(a)))
#     assert lps(a) == linear(permute(sub_bytes(a)))

'''------------------------------------------------------------------------'''

'''-----------------E-shifr test----------------------------------------'''


def test_E_full_rounds_on_rfc_example_be():
    iv = b"\x01" * 64
    K1 = lps(iv)
    m = bytes.fromhex(
        "01323130393837363534333231303938"
        "37363534333231303938373635343332"
        "31303938373635343332313039383736"
        "35343332313039383736353433323130"
    )
    got_le = E(K1, m)

    # Переводим каждый 8-байтный блок в big-endian
    got_be = b"".join(
        got_le[i:i+8][::-1] for i in range(0, 64, 8)
    )

    expected = bytes.fromhex(
        "fc221dc8b814fc27a4de079d10097600"
        "209e5375776898961f70bded0647bd8f"
        "1664cfa8bb8d8ff1e0df3e621568b66a"
        "a075064b0e81cce132c8d1475809ebd2"
    )
    assert got_be == expected, (
        f"\nE(K1,m) mismatch (big-endian):\n"
        f" got:      {got_be.hex()}\n"
        f" expected: {expected.hex()}"
    )
