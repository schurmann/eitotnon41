import sys
from hashlib import sha1
import pprint
import math

def build_merkle_tree(leafs: list, path_i: int, path: list = []) -> list:
    if len(leafs) == 1:
        return [leafs]
    leafs = padded(leafs)
    print("path_i:",path_i)
    path.append(find_pathnode(leafs, path_i))
    nextlayer = []
    for i in range(0, len(leafs), 2):
        # if start_index < i + 2:
        #     #Paths starts here
        #     if start_index % 2 == 0:
        #         path.append('R' + bytes.hex(leafs[start_index + 1]))
        #     else:
        #         path.append('L' + bytes.hex(leafs[start_index + 1]))
        parent_node = build_parent(leafs[i], leafs[i+1])
        nextlayer.append(parent_node)
    path_parent_i = math.floor(path_i/2)
    return [leafs] + build_merkle_tree(nextlayer, path_parent_i, path)

def find_pathnode(layer, i):
    assert(len(layer) > 1)
    assert(i < len(layer))
    if i % 2 == 0:
        return 'R' + bytes.hex(layer[i + 1])
    else:
        return 'L' + bytes.hex(layer[i - 1])

def build_parent(l: bytearray, r: bytearray) -> bytearray:
    return sha1(l + r).digest()

def padded(l: list):
    return l + [l[-1]] if len(l) % 2 != 0 else l

def print_tree(tree: list):
    width = len(tree[0])
    for depth, layer in enumerate(reversed(tree)):
        print("".join([" " + n.hex()[:3] for n in layer]))
        print("")


if __name__ == '__main__':
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        inputs = [line.strip() for line in f]
        leaf_index = inputs[0]
        depth_index = inputs[1]
        leafs = inputs[2:]
        byteleafs = [bytes.fromhex(l) for l in leafs]
        path = []
        # tree = build_merkle_tree(byteleafs, int(leaf_index), path)
        tree = build_merkle_tree(byteleafs, 9, path)
        # for layer in tree:
        #     print('layer size:',len(layer),'type:',type(layer), 'element type:', type(layer[0]))
        print_tree(tree)
        print('path:')
        pprint.pprint(path)
        print('depth',depth_index, ':', path[-int(depth_index)])
        f.close()
