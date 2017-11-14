import random
import math
from hashlib import sha256

RANDCEIL = 2048
N = 123
K = 1000

def rand() -> int:
    return random.randint(0, RANDCEIL) % N

class Bank:
    def __init__(self):
        self.bees = []

    def verify_quads(self, chosen_quads: list) -> bool:
        pass

    def choose_and_remember(self, bs: list) -> list:
        self.bees = bs
        return random.sample(range(0, 2*K), K)

class Customer:
    def __init__(self):
        self.ID = 1
        self.quads = []
        self.bees = []

    def __f(self, a: bytes, b: bytes) -> int:
        return int.from_bytes((a + b), byteorder='big')

    def gen_quads(self, k: int) -> list:
        self.quads = [(rand(), rand(), rand(), rand()) for i in range(2*k)]

    def __make_x(self, a: int, c: int) -> bytes:
        return sha256(a.to_bytes(2, byteorder='big') + c.to_bytes(2, byteorder='big')).digest()

    def __make_y(self, a: int, d: int, identifier: int) -> bytes:
        return sha256((a ^ identifier).to_bytes(2, byteorder='big') + d.to_bytes(2, byteorder='big')).digest()

    def __make_b():
        return (math.pow(r, 3) * f_out) % n


    def make_bees(self, r: int, f_out: int, n: int) -> int:
        self.bees = [self__make_b(math.pow(r, 3), self.__f(self.__make_x(a, c), self.__make_y(a, d, ID)), N) for (a, c, d, r) in self.quads]

if __name__ == '__main__':
    bank = Bank()
    customer = Customer()
    customer.gen_quads(K)
    print(customer.quads)
    #bs = 
    #indexes = bank.choose_and_remember(bs)
    #chosen_quads = [quads[index] for index in indexes]
    #bank.verify_quads(chosen_quads)
