#!/usr/bin/python3
import sys
import base64

for line in sys.stdin:
    print(base64.b64decode(line).hex())

