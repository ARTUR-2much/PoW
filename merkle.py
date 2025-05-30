from streebog import digest


def _pair_hash(left: bytes, right: bytes) -> bytes:
    """ H(left ‖ right)  → 32-байтовый узел """
    return digest(left + right)


def calc_root(leaves: list[bytes], *, duplicate_last: bool = True) -> bytes:
    """
    Вычисляет Merkle-корень.
    :param leaves: список 32-байтовых листьев
    :param duplicate_last: True  – дублировать последний,
                           False – «поднимать» одиночный
    """
    assert leaves, "leaves must not be empty"
    assert all(len(x) == 32 for x in leaves), "every leaf must be 32 bytes"

    level = leaves[:]                       # копия первого уровня
    while len(level) > 1:
        if len(level) % 2 == 1:             # нечётное количество
            if duplicate_last:
                level.append(level[-1])     # BTC-стиль: дублируем

        nxt: list[bytes] = []
        i = 0
        while i < len(level):
            # если последний остался без пары и duplicate_last == False –
            # просто переносим его наверх
            if i + 1 == len(level):
                nxt.append(level[i])
                i += 1
            else:
                nxt.append(_pair_hash(level[i], level[i + 1]))
                i += 2
        level = nxt

    return level[0]