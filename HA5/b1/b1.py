from asn1crypto.core import Sequence, Integer
from asn1crypto.keys import RSAPrivateKey
from asn1crypto import pem
from sys import argv

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
