import pytest
from schnorr import PrivateKey, PublicKey, p, q, g, a
from gspch import PRNG
from streebog import digest

# один и тот же seed → детерминируемая подпись
@pytest.fixture
def keypair():
    prng = PRNG(digest(b"deterministic-seed"))
    sk = PrivateKey.generate(prng)
    pk = PublicKey(sk.y)
    return sk, pk

def test_sign_and_verify_ok(keypair):
    sk, pk = keypair
    msg = b"Hello, Schnorr!"
    sig = sk.sign(msg)
    assert pk.verify(msg, sig)

def test_bad_message_rejects(keypair):
    sk, pk = keypair
    sig = sk.sign(b"msg-1")
    assert not pk.verify(b"msg-2", sig)


def test_melochi():
    assert (p - 1) % q == 0, "q не делит p-1"
    g = pow(a, (p - 1) // q, p)
    assert g != 1 and pow(g, q, p) == 1, "g неверен"


def test_reuse_nonce_replays_sig():
    from gspch import PRNG
    from schnorr import PrivateKey, PublicKey, _hash_mod_q

    prng = PRNG(digest(b"\x01"))          # повторяемое состояние
    sk = PrivateKey.generate(prng)
    pk = PublicKey(sk.y)

    r = prng.get_int(q)
    R = pow(g, r, p)

    msg = b"same"
    e = _hash_mod_q(R.to_bytes(64,"big")+pk.y.to_bytes(64,"big")+msg)
    s1 = (r + e*sk.x) % q
    s2 = (r + e*sk.x) % q         # тот же r ⇒ ровно тот же s

    assert (R, s1) == (R, s2)
    assert pk.verify(msg,(R,s1))
