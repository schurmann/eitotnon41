import sys
from hashlib import sha1
import pprint

def build_merkle_tree(leafs: list) -> list:
    if len(leafs) == 1:
        return [leafs]
    leafs = padded(leafs)
    nextlayer = []
    for i in range(0, len(leafs), 2):
        parent_node = build_parent(leafs[i], leafs[i+1])
        nextlayer.append(parent_node)
    return [leafs] + build_merkle_tree(nextlayer)

def build_parent(l: bytearray, r: bytearray) -> bytearray:
    return sha1(l + r).digest()

def padded(l: list):
    return l + [l[-1]] if len(l) % 2 != 0 else l

if __name__ == '__main__':
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        inputs = [line.strip() for line in f]
        leaf_index = inputs[0]
        depth_index = inputs[1]
        leafs = inputs[2:]
        byteleafs = [bytes.fromhex(l) for l in leafs]
        tree = build_merkle_tree(byteleafs)
        for layer in tree:
            print('layer size:',len(layer),'type:',type(layer), 'element type:', type(layer[0]))
        f.close()
