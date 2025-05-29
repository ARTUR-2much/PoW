#  Подпись Шнорра (key-prefixed) над полем  Zp  c подгруппой порядка q
#  p, q, a  взяты из примера A.3 ГОСТ-Р 34.10-94, g = a ^ ((p-1)/q)  (mod p)
# ---------------------------------------------------------------------------
from dataclasses import dataclass
from math import ceil
from gspch import PRNG
from streebog import digest


p = int("EE8172AE8996608FB69359B89EB82A69854510E2977A4D63BC97322CE5DC3386EA0A12B343E9190F23177539845839786BB0C345D165976EF2195EC9B1C379E3", 16)
q = int("98915E7EC8265EDFCDA31E88F24809DDB064BDC7285DD50D7289F0AC6F49DD2D", 16)
a = int("9E96031500C8774A869582D4AFDE2127AFAD2538B4B6270A6F7C8837B50D50F206755984A49E509304D648BE2AB5AAB18EBE2CD46AC3D8495B142AA6CE23E21C", 16)


assert (p - 1) % q == 0, "q не делит p-1"

g = pow(a, (p - 1) // q, p)
assert 1 < g < p and pow(g, q, p) == 1, "g некорректен"

_L = ceil(p.bit_length() / 8)

def _hash_mod_q(data: bytes) -> int:
    return int.from_bytes(digest(data), "big") % q


@dataclass(frozen=True)
class PrivateKey:
    x: int          # секрет
    y: int          # g^x mod p
    prng: PRNG

    @classmethod
    def generate(cls, prng: PRNG) -> "PrivateKey":
        x = prng.get_int(q) or 1
        y = pow(g, x, p)
        return cls(x, y, prng)


    def sign(self, msg: bytes) -> tuple[int, int]:
        r = self.prng.get_int(q) or 1
        R = pow(g, r, p)

        e = _hash_mod_q(
            R.to_bytes(_L, "big") +
            self.y.to_bytes(_L, "big") +   #   ← key-prefixed
            msg
        )
        s = (r + e * self.x) % q
        return R, s


@dataclass(frozen=True)
class PublicKey:
    y: int      # g^x mod p

    def verify(self, msg: bytes, sig: tuple[int, int]) -> bool:
        R, s = sig
        if not (1 <= R < p and 1 <= s < q):
            return False

        e = _hash_mod_q(
            R.to_bytes(_L, "big") +
            self.y.to_bytes(_L, "big") +
            msg
        )
        lhs = pow(g, s, p)
        rhs = (R * pow(self.y, e, p)) % p
        return lhs == rhs