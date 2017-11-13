#! /usr/bin/env python
import hashlib
import binascii


def int_to_hex(n: int):
    return hex(n)


def hex_to_int(s: str) -> int:
    return int(s, 16)


def int_to_bytes(n: int, size=4) -> bytearray:
    return n.to_bytes(4 if size is None else size, byteorder='big')


def bytes_to_int(arr: bytearray) -> int:
    return int.from_bytes(arr, byteorder='big')


def hex_to_bytes(s: str) -> bytearray:
    return binascii.unhexlify(s)


def bytes_to_hex(arr: bytearray):
    return binascii.hexlify(arr).decode('utf-8')


def sha1(bts: bytearray) -> bytearray:
    return hashlib.sha1(bts).digest()


h = '0123456789abcdef'
byte_result = hex_to_bytes(h)
int_result = bytes_to_int(byte_result)
hash_result = sha1(int_to_bytes(int_result, size=8))
print(bytes_to_int(hash_result))
