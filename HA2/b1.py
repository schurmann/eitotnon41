import random

def pad(x:str, n:int) -> str:
    if len(x) < n:
        return '0'*(n - len(x)) + x
    else:
        return x

def check(sa:int, sb:int, da:int, db:int, m:int, b:bool) -> str:
    x = sa ^ sb
    if b:
        x ^= m
        return pad(hex(x)[2:], 4)
    else:
        ans = x ^ da ^ db
        return pad(hex(x)[2:], 4) + pad(hex(ans)[2:], 4)


if __name__ == '__main__':
    assert(check(0x0c73, 0x80c1, 0xa2a9, 0x92f5, 0x9b57, 0) == '8cb2bcee')
    assert(check(0x27c2, 0x0879, 0x35f4, 0x1a4d, 0x27bc, 1) == '0807')
    print(check(sa=0xd75c, sb=0xee87, da=0xc568, db=0xfcb3, m=0x4674, b=1))
    print(check(sa=0x75f5, sb=0xb1ac, da=0x67c1, db=0xa398, m=0x00bc, b=0x0))
    print(check(sa=0xbf0d, sb=0x3c99, da=0x186f, db=0x2ead, m=0x62ab, b=0x0))
