#!/usr/bin/env python3
import re
import sys

with open(sys.argv[1], "r") as f:
    scan = f.readlines()

for line in scan:
    if 'open tcp' in line:
        parts = line.strip().split()
        host = parts[3]
        port = parts[2]
        if '443' in port:
            print("https://" + host + ":" + port)
        else:
            print("http://" + host + ":" + port)

