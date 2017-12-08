from hashlib import sha1
from math import ceil
from sys import exit

def i2osp(x:int, xlen:int) -> bytes:
    assert x >= 0
    if x >= 256**xlen:
        print('integer too large')
        exit()
    return x.to_bytes(xlen, byteorder='big', signed=False)

def test_i2osp():
    assert(i2osp(20,4) == bytes([0]*3 + [20]))

def mgf1(mgfseed:bytes, masklen:int, hashalg=sha1):
    hLen = hashalg().digest_size
    if masklen > 2**32*hLen:
        print('mask too long')
        exit()
    T = b''
    for counter in range(ceil(masklen / hLen)):
        C = i2osp(counter, 4)
        T = T + hashalg(mgfseed + C).digest()
    return T[:masklen]

def xor(x: bytes, y: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(x, y))

def test_xor():
    # 11 xor 01 == 10
    assert xor(b'\x03',b'\x01') == b'\x02'

def OAEP_encode(m: str, seed: str, L='', hashalg=sha1) -> str:
    m = bytes.fromhex(m)
    seed = bytes.fromhex(seed)
    k = 128
    mLen = len(m)
    hLen = hashalg().digest_size
    lHash = hashalg(L.encode()).digest()
    PS = b'\x00'*(k - mLen - 2*hLen - 2)
    DB = lHash + PS + b'\x01' + m
    dbMask = mgf1(seed, k - hLen - 1)
    maskedDB = xor(DB, dbMask)
    seedMask = mgf1(maskedDB, hLen)
    maskedSeed = xor(seed, seedMask)
    EM = b'\x00' + maskedSeed + maskedDB
    return EM.hex()

def dissassemble_DB(DB: bytes, hLen: int, lHash: bytes):
    err_msg = 'decryption error'
    lHash_ = DB[:hLen]
    if lHash_ != lHash_:
        raise RuntimeError(err_msg)
        
    PS_start = DB.find(b'\x00', hLen)
    PS_end = DB.find(b'\x01', PS_start)
    if PS_end == -1:
        raise RuntimeError(err_msg)
    PS = DB[PS_start:PS_end]

    M = DB[PS_end + 1:]
    return lHash_, PS, M
    

def OAEP_decode(em: str, L='', hashalg=sha1) -> str:
    em = bytes.fromhex(em)
    k = 128
    hLen = hashalg().digest_size
    lHash = hashalg(L.encode()).digest()
    Y, maskedSeed, maskedDB = em[:1], em[1:hLen + 1], em[hLen + 1:]
    seedMask = mgf1(maskedDB, hLen)
    seed = xor(maskedSeed, seedMask)
    dbMask = mgf1(seed, k - hLen - 1)
    DB = xor(maskedDB, dbMask)
    lHash_, PS, M = dissassemble_DB(DB, hLen, lHash)
    return M.hex()


def test_mgf1():
    assert(mgf1(bytes.fromhex('0123456789abcdef'),30) == bytes.fromhex('18a65e36189833d99e55a68dedda1cce13a494c947817d25dc80d9b4586a'))
    
def test_OAEP_encode():
    M = 'fd5507e917ecbe833878'
    seed = '1e652ec152d0bfcd65190ffc604c0933d0423381'
    EM = '0000255975c743f5f11ab5e450825d93b52a160aeef9d3778a18b7aa067f90b2178406fa1e1bf77f03f86629dd5607d11b9961707736c2d16e7c668b367890bc6ef1745396404ba7832b1cdfb0388ef601947fc0aff1fd2dcd279dabde9b10bfc51f40e13fb29ed5101dbcb044e6232e6371935c8347286db25c9ee20351ee82'
    assert(OAEP_encode(M, seed) == EM)

def test_OAEP_decode():
    M = 'fd5507e917ecbe833878'
    EM = '0000255975c743f5f11ab5e450825d93b52a160aeef9d3778a18b7aa067f90b2178406fa1e1bf77f03f86629dd5607d11b9961707736c2d16e7c668b367890bc6ef1745396404ba7832b1cdfb0388ef601947fc0aff1fd2dcd279dabde9b10bfc51f40e13fb29ed5101dbcb044e6232e6371935c8347286db25c9ee20351ee82'
    assert(OAEP_decode(EM) == M)

###Test quiz###
print(mgf1(b'9b4bdfb2c796f1c16d0c0772a5848b67457e87891dbc8214', 21).hex()) #Failed
print(OAEP_encode('c107782954829b34dc531c14b40e9ea482578f988b719497aa0687', '1e652ec152d0bfcd65190ffc604c0933d0423381')) #Failed
print(OAEP_decode('0063b462be5e84d382c86eb6725f70e59cd12c0060f9d3778a18b7aa067f90b2178406fa1e1bf77f03f86629dd5607d11b9961707736c2d16e7c668b367890bc6ef1745396404ba7832b1cdfb0388ef601947fc0aff1fd2dcd279dabde9b10bfc51efc06d40d25f96bd0f4c5d88f32c7d33dbc20f8a528b77f0c16a7b4dcdd8f')) #Passed
