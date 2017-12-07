from scipy.interpolate import lagrange
from numpy import poly1d


def deactivate(poly:poly1d, master_shares:dict, my_shares:list, my_id:int) -> int:
    my_master_share = sum(my_shares + [poly(my_id)])
    master_shares[my_id] = my_master_share
    master_x = list(master_shares)
    master_y = [master_shares[x] for x in master_x]
    master_poly = lagrange(master_x, master_y)
    return int(master_poly(0)) #TODO round? ceil? floor?

def test_example():
    code = deactivate(
        my_id=1,
        poly=poly1d([5, 1, 11, 8, 13]),
        master_shares={
            2: 2782,
            4: 30822,
            5: 70960,
            7: 256422,
            },
        my_shares=[ 75, 75, 54, 52, 77, 54, 43 ],
    )
    assert code == 110

def test_quiz():
    code1 = deactivate(
            poly=poly1d([6,11,20,20]),
            my_id=1,
            my_shares=[63,49,49,54,43],
            master_shares={
                3: 2199,
                4: 4389,
                6: 12585
                }
            )
    code2 = deactivate(
            poly=poly1d([15, 19, 13, 18, 20]),
            my_id=1,
            my_shares=[34, 48, 45, 39, 24],
            master_shares={
                2: 1908,
                3: 7677,
                5: 50751,
                6: 101700
                }
            )
    code3 = deactivate(
            poly=poly1d([5, 19, 9]),
            my_id=1,
            my_shares=[37, 18, 40, 44, 28],
            master_shares={
                4: 1385,
                5: 2028
                }
            )
    assert code1 == 93
    assert code2 == 36
    assert code3 == 53

if __name__ == '__main__':
    t_quiz()
