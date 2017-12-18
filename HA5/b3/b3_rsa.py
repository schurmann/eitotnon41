e = 65537
def gen_skey_params(p, q):
    par = {'e': e}
    par['p'] = p
    par['q'] = q
    par['n'] = p*q
    r = (p-1) * (q-1)
    par['d'] = modinv(e, r)
    par['exp1'] = par['d'] % (p-1)
    par['exp2'] = par['d'] % (q-1)
    par['coeff'] = modinv(q, p)
    return par

# def multiplicative_inverse(e, phi):
#     #d ≡ e^(-1) (mod r)
#     t, new_t = 0, 0
#     r, new_r = phi, e
#     while new_r != 0:
#         quotient = r // new_r
#         t, new_t = new_t, t - quotient * new_t
#         r, new_r = new_r, r - quotient * new_r
#     if r > 1:
#         print('e is not invertible')
#         return None
#     if t < 0:
#         t = t + n
#     return t

def egcd(e, b):
    if e == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % e, e)
        return (g, x - (b // e) * y, y)

def modinv(e, r):
    g, x, y = egcd(e, r)
    if g != 1:
        print('no modular inverse!')
        return None
    else:
        return x % r

def test_params():
    par = gen_skey_params(p=2530368937, q=2612592767)
    assert par['n'] == 6610823582647678679
    assert par['d'] == 3920879998437651233
    assert par['exp1'] == 2013885953
    assert par['exp2'] == 1498103913
    assert par['coeff'] == 1490876340

def test_inv():
    r = 6610823577504717000
    d = modinv(r, e)
    print(d)

if __name__ == '__main__':
    test_inv()
