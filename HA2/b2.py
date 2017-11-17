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


def learning_phase(target_ip:str, mix_ip:str, m:int, filename:str) -> list:
    cap = savefile.load_savefile(open(filename, 'rb'), layers=2, verbose=True)
    send_indices = [
            i
            for i, p in enumerate(cap.packets)
            if p.packet.payload.src.decode('UTF8') == target_ip
    ]
    batches = [next_batch(i, mix_ip, list(cap.packets)) for i in send_indices]
    return [ set(map(lambda x: x.packet.payload.dst.decode('UTF8'), batch)) for batch in batches ]

def find_partners(target_ip:str, mix_ip:str, m:int, filename:str):
    batchsets = learning_phase(target_ip, mix_ip, m, filename)
    disjoint_batches, joint_batches = separate_disjoint_batches(batchsets, m)
    valid_rs = [r for r in joint_batches if len(joint_with(r, disjoint_batches)) == 1]
    for r in valid_rs:
        joint_dbatches = joint_with(r, disjoint_batches)
        assert(len(joint_dbatches) == 1)
        dbatch = joint_dbatches[0]
        dbatch.intersection_update(r)
    for b in disjoint_batches:
        assert(len(b) == 1)
    partners = [list(b)[0] for b in disjoint_batches]
    return partners


def disjoint(b1:set, b2:set) -> bool:
    b =  len(b1.intersection(b2)) == 0
    return b

def joint_with(b:set, others:list) -> list:
    return [o for o in others if not disjoint(b, o)]


def separate_disjoint_batches(batchsets: list, m: int):
    disjoint_indices = []
    # for i in range(0, len(batchsets)):
    #     for j in range(i + 1, len(batchsets)):
    #         if disjoint(batchsets[i], batchsets[j]):
    #            break
    #     disjoint.append(i)
    for i, batch in enumerate(batchsets):
        if len(joint_with(batch, [batchsets[i] for i in disjoint_indices])) == 0:
            disjoint_indices.append(i)
            if len(disjoint_indices) == m:
                break
    disjoint_batches = []
    joint_batches = []
    for i, b in enumerate(batchsets):
        if i in disjoint_indices:
            disjoint_batches.append(b)
        else:
            joint_batches.append(b)
    return disjoint_batches, joint_batches

def exclude_phase(r: set, others: list):
    return r.intersection(set(others[0])).intersection(set(others[1]))
        
if __name__ == '__main__':
    partners = find_partners('159.237.13.37', '94.147.150.188', 2, 'cia.log.1337.pcap')
    ans = sum([int(''.join([hex(int(i))[2:] for i in ip.split(r'.')]), 16) for ip in partners])
    print(ans)
