from asn1crypto.core import Sequence, Integer
from asn1crypto.keys import RSAPrivateKey
from asn1crypto import pem
from sys import argv
from asn import byte_size, int_to_bytes, encode_int

# def byte_size(i: int) -> int:
#     return 1 if i == 0 else int(log(i, 256)) + 1

# def int_to_bytes(i: int) -> bytes:
#     return i.to_bytes(byte_size(i), byteorder='big')

def load_key(filename:str) -> RSAPrivateKey:
    with open(filename, 'rb') as f:
        pembytes = f.read()
        if pem.detect(pembytes):
            _, _, raw = pem.unarmor(pembytes)
            return RSAPrivateKey.load(raw)
        else:
            print('bad pem!')
            sys.exit(1)

def regen_modulo(k:RSAPrivateKey) -> RSAPrivateKey:
    p1 = int.from_bytes(k['prime1'].contents, byteorder='big')
    p2 = int.from_bytes(k['prime2'].contents, byteorder='big')
    mod = p1 * p2
    # k['modulus'] = Integer.load(bytes.fromhex(encode_int(mod)))
    k['modulus'] = mod
    return k

def write_key(filename:str, k:RSAPrivateKey):
    with open(filename, 'wb') as f:
        pem_content = pem.armor('RSA PRIVATE KEY', k.dump())
        f.write(pem_content)

if __name__ == '__main__':
    print(argv)
    k = load_key(argv[1])
    k = regen_modulo(k)
    write_key(argv[2], k)
