from hashlib import sha256
import random

K_SIZE = 16

def h(v:str, k:str, x: int) -> str:
    vk_bytes = bytes.fromhex((v + k).zfill(6))
    return bin(int.from_bytes(sha256(vk_bytes).digest(), byteorder='big'))[2:2+x]

def gen_k() -> int:
    return random.getrandbits(K_SIZE)

def find_binding_prob() -> float:
    for x in range(1, 10):
        pass

def find_concealing_prob() -> float:
    pass

if __name__ == '__main__':
    k = gen_k()
    print(h('1', str(k), 2))

