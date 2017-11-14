import random

def check(sa: int, sb:int, da:int, db:int, m:int, b:bool):
    x = sa ^ sb
    ans = x ^ da ^ db
    return hex(x)[2:] + hex(ans)[2:]


if __name__ == '__main__':
    pass
