import hashlib
import random
import pickle
import time
import math
from collections import defaultdict

def throw_ball(counter, conf):
    ball = counter.to_bytes(4, byteorder='big') + conf['nonce']
    hit_bin = hashlib.sha1(ball)
    hit_bit = bin(int(hit_bin.hexdigest(), base=16))[-conf['u']:]
    return hit_bit, ball

def gen_coins(conf):
    starttime = time.time()
    bins = defaultdict(lambda: [])
    counter = 0
    found = set()
    while len(found) < conf['c']:
        hit_bin, ball = throw_ball(counter, conf)
        bins[hit_bin].append(ball)
        if len(bins[hit_bin]) >= conf['k']:
            found.add(hit_bin)
        counter += 1
    return counter-1

def save_data(data):
     pickle.dump(data, open('b2.log', 'wb'))
     print('data saved', time.time())

def mean(vals):
    return sum(vals)/len(vals)

def stdev(vals):
    m = mean(vals)
    return math.sqrt(sum([(x - m) ** 2 for x in vals]) / (len(vals) - 1))

def interval(vals, config):
    m = mean(vals)
    dev = config['l'] * stdev(vals) / math.sqrt(len(vals))
    return m - dev, m + dev


if __name__ == '__main__':
    durations = []
    while True:
        experiment_config = {
            'u' : 16,
            'k' : 4,
            'c' : 1,
            'w' : 578,
            'l' : 3.66,
            'nonce' : random.randint(0, 10000).to_bytes(4, byteorder='big')
        }
        durations.append(gen_coins(experiment_config))
        print('mean:', mean(durations))
        if len(durations) > 1:
            i_start, i_end = interval(durations, experiment_config)
            print('interval width:', i_end - i_start)
            if (i_end - i_start) < experiment_config['w']:
                break
