from pcapfile import savefile
from pprint import pprint

def next_batch(index, mix_ip, packets):
    print('next_batch index = ', index)
    print('len(packets):',len(packets))
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
    for i in range(0, len(batchips)):
        for j in range(i + 1, len(batchips)):
            if len(batchips[i].intersect(batchips[j])) = 0:
                #save i
                pass


def get_disjunct_sets(batchips: list):
    pass
        

    pprint(batchips)

if __name__ == '__main__':
    find_partners('159.237.13.37', '94.147.150.188', 2, 'cia.log.1337.pcap')
