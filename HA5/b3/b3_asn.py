from b3_rsa import gen_skey_params
import base64
from math import log

def bin_to_hex(bin_s: str) -> str:
    return hex(int(bin_s, 2))[2:]

# def byte_length(i: int) -> int:
#     return len(hex(i)[2:]) // 2

def bytelen(i: int) -> int:
    return 1 if i == 0 else (int(log(i, 256)) + 1)

def test_bytelen():
    assert bytelen(0x0) == 1
    assert bytelen(0x52) == 1
    assert bytelen(0xaaaa) == 2
    assert bytelen(0xffff) == 2
    assert bytelen(0x12345) == 3

def get_val(i:int) -> str:
    val = hex(i)[2:]
    if len(val) % 2 != 0:
        val = '0' + val
    return val

def get_len(i: int):
    val = bytes.fromhex(get_val(i))
    l = len(val)
    if l > 127:
        req_bytes = 1 if l == 0 else (int(log(l, 256)) + 1)
        #TODO felmeddelande för för stora tal
        lenlen = (0x80 + req_bytes).to_bytes(1, byteorder='big')
        return lenlen + l.to_bytes(req_bytes, byteorder='big')
    return l.to_bytes(1, byteorder='big')

# def get_len(i:int):
#     val = get_val(i)
#     length = len(val) // 2
#     if len(bin(i)[2:]) % 8 == 0:
#         val = '00' + val
#         length += 1
#     if length > 127:
#         #Use long defintive form
#         len_length = byte_length(length)
#         length = bin_to_hex('1' + bin(len_length)[2:].zfill(7) + bin(length)[2:])
#     else:
#         #Use short definite form
#         length = bin_to_hex('0' + bin(length)[2:])
#     if len(length) % 2 != 0:
#         length = '0' + length
#     print(length)
#     return length

def encode_int(i:int) -> str:
    type_ = "02"
    val = get_val(i)
    if len(bin(i)[2:]) % 8 == 0:
        val = '00' + val
    length = get_len(i).hex()
    ans = type_ + length + val
    return ans

def encode_seq(elements):
    type_ = '30'
    val = ''.join(elements)
    length = get_len(int(val, 16))
    return type_ + length + val


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
    #print(encoded, '\n')
    #print(base64.b64encode(bytes.fromhex(encoded)))
