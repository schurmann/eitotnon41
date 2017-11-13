import random
import math
from hashlib import sha256

RANDCEIL = 2048
N = 123
K = 1000
ID = 1

class Bank:
    bees = []

    def verify_quads(self, chosen_quads: list) -> bool:
        pass

    def choose_and_remember(self, bs: list) -> list:
        bees = bs
        return random.sample(range(0, 2*K), K)


def f(a: bytes, b: bytes) -> int:
    return int.from_bytes((a + b), byteorder='big')

def rand() -> int:
    return random.randint(0, RANDCEIL) % N

def gen_quads(k: int) -> list:
    return [(rand(), rand(), rand(), rand()) for i in range(2*k)]

def make_x(a: int, c: int) -> bytes:
    return sha256(a.to_bytes(2, byteorder='big') + c.to_bytes(2, byteorder='big')).digest()

def make_y(a: int, d: int, identifier: int) -> bytes:
    return sha256((a ^ identifier).to_bytes(2, byteorder='big') + d.to_bytes(2, byteorder='big')).digest()

def make_b(r: int, f_out: int, n: int) -> int:
    return (math.pow(r, 3) * f_out) % n

if __name__ == '__main__':
    bank = Bank()
    quads = gen_quads(K)
    bs = [make_b(math.pow(r, 3), f(make_x(a, c), make_y(a, d, ID)), N) for (a, c, d, r) in quads]
    indexes = bank.choose_and_remember(bs)
    chosen_quads = [quads[index] for index in indexes]
    bank.verify_quads(chosen_quads)
