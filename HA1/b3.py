from hashlib import sha1
import sys

def compute_merkel_root(leaf: str, path: list):
    if len(path) == 0:
        return leaf
    else:
        direction = path[0][0]
        othernode = path[0][1:]
        return compute_merkel_root(combine_nodes(bytearray.fromhex(leaf), bytearray.fromhex(othernode), direction), path[1:])

def combine_nodes(leaf: bytearray, othernode: bytearray, direction) -> str:
    new_node = leaf + othernode if direction == 'R' else othernode + leaf
    md = sha1(new_node).hexdigest()
    return md

def spv_node(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        inputs = [line.strip() for line in f]
        leaf = inputs[0]
        path = inputs[1:]
        root = compute_merkel_root(leaf, path)
        print('Result: ', root)


if __name__ == '__main__':
    spv_node(sys.argv[1])
