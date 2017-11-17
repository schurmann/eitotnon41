from pcapfile import savefile
from pprint import pprint

def next_batch(index, mix_ip, packets):
    while index < len(packets) and packets[index].packet.payload.src.decode('UTF8') != mix_ip:
        index += 1
    batch = []
    while index < len(packets) and packets[index].packet.payload.src.decode('UTF8') == mix_ip: 
        batch.append(packets[index])
        index += 1
    return batch


def find_partners(target_ip:str, mix_ip:str, m:int, filename:str):
    cap = savefile.load_savefile(open(filename, 'rb'), layers=2, verbose=True)
    send_indices = [
            i
            for i, p in enumerate(cap.packets)
            if p.packet.payload.src.decode('UTF8') == target_ip
    ]
    batches = [next_batch(i, mix_ip, list(cap.packets)) for i in send_indices]
    batchips = [ set(map(lambda x: x.packet.payload.dst.decode('UTF8'), batch)) for batch in batches ]
    disjunct_ips = get_disjunct_sets(batchips) #indexes for disjoint sets
    return [batchips[i] for i in disjunct_ips]


def disjoint(b1:set, b2:set) -> bool:
    b =  len(b1.intersection(b2)) == 0
    return b


def get_disjunct_sets(batchips: list):
    disjunct_ips = []
    for i in range(0, len(batchips)):
        for j in range(i + 1, len(batchips)):
            if disjoint(batchips[i], batchips[j]):
               break
        disjunct_ips.append(i)
    return disjunct_ips

def exclude_phase(r: set, others: list):
    return r.intersection(set(others[0])).intersection(set(others[1]))
        

if __name__ == '__main__':
    ip_sets = find_partners('159.237.13.37', '94.147.150.188', 2, 'cia.log.1337.pcap')
    ip_sets = ip_sets[:2] if len(ip_sets) > 2 else ip_sets
    r = ip_sets[-1]
    ans = exclude_phase(r, ip_sets)
    print(ans)
