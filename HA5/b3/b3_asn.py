from b3_rsa import gen_skey_params
import base64
from math import log

def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, byteorder='big')

def byte_size(i: int) -> int:
    return 1 if i == 0 else int(log(i, 256)) + 1

def int_to_bytes(i: int) -> bytes:
    return i.to_bytes(byte_size(i), byteorder='big')

def test_byte_size():
    assert byte_size(0x0) == 1
    assert byte_size(0x52) == 1
    assert byte_size(0xff) == 1
    assert byte_size(0xaaaa) == 2
    assert byte_size(0xffff) == 2
    assert byte_size(0x12345) == 3


def test_get_len():
    assert get_len(b'\x00').hex() == '01'
    assert get_len(b'\x7f').hex() == '01'
    assert get_len(b'\x00'*131).hex() == '8183' #131 bytes

def get_len(b: bytes) -> bytes:
    l = len(b)
    if l > 127:
        req_bytes = byte_size(l)
        #TODO felmeddelande för för stora tal
        lenlen = int_to_bytes(0x80 | req_bytes)
        return lenlen + int_to_bytes(l)
    return int_to_bytes(l)

def encode_int(i:int) -> str:
    t = b'\x02'
    v = int_to_bytes(i)
    if len(bin(i)[2:]) % 8 == 0:
        v = b'\x00' + v
    l = get_len(v)
    return (t + l + v).hex()

def encode_seq(elements):
    t = b'\x30'
    v = bytes.fromhex(''.join(elements))
    l = get_len(v)
    return (t + l + v).hex()


def encode_rsa(params):
             # version
    fields = [encode_int(0)] + [
                encode_int(params[label])
                for label in ['n','e','d','p','q','exp1','exp2','coeff']
            ]
    return encode_seq(fields)


def test_encode_int():
    # sdf
    assert encode_int(2530368937) == '02050096d25da9'
    # ldf
    assert encode_int(161863091426469985001358176493540241719547661391527305133576978132107887717901972545655469921112454527920502763568908799229786534949082469136818503316047702610019730504769581772016806386178260077157969035841180863069299401978140025225333279044855057641079117234814239380100022886557142183337228046784055073741) == '02818100e6802d70d04dea6724d9398116cbdad4a7d824a6846432d8cae83ea9be7027f7bf80082fd9b6ed5a36656dc92e1141290c9437fec219f981c255599849e1b65c64d4184a96f4c0af287577997be19cf500a7997f2e362a2ef263e75af3be6611ded3d18e5e9c02aaee4484593017806531d9a9507c2241806e7cfa7298c9dbcd'

def test_encode_rsa():
    p, q = 2530368937, 2612592767
    params = gen_skey_params(p, q)
    assert encode_int(params['n']) == '02085bbe5d05d47d76d7' 
    assert encode_int(params['e']) == '0203010001' 
    assert encode_int(params['d']) == '02083669c395b9cf7321' 
    assert encode_int(params['p']) == '02050096d25da9' 
    assert encode_int(params['q']) == '0205009bb9007f' 
    assert encode_int(params['exp1']) == '020478097601' 
    assert encode_int(params['exp2']) == '0204594b4069' 
    assert encode_int(params['coeff']) == '020458dcf7b4' 
    assert base64.b64encode(bytes.fromhex(encode_rsa(params))) == b'MDwCAQACCFu+XQXUfXbXAgMBAAECCDZpw5W5z3MhAgUAltJdqQIFAJu5AH8CBHgJdgECBFlLQGkCBFjc97Q='


if __name__ == '__main__':
    p, q = 139721121696950524826588106850589277149201407609721772094240512732263435522747938311240453050931930261483801083660740974606647762343797901776568952627044034430252415109426271529273025919247232149498325412099418785867055970264559033471714066901728022294156913563009971882292507967574638004022912842160046962763, 141482624370070397331659016840167171669762175617573550670131965177212458081250216130985545188965601581445995499595853199665045326236858265192627970970480636850683227427420000655754305398076045013588894161738893242561531526805416653594689480170103763171879023351810966896841177322118521251310975456956247827719
    params = gen_skey_params(p, q)
    encoded = encode_rsa(params).strip()
    print(base64.b64encode(bytes.fromhex(encoded)).decode('utf8'))
