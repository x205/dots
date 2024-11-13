#!/usr/bin/env python3

import sys
import re

#fin = set()

def change(line):
    if re.search(r'[^.!]\..{3,4}$', line) and not re.search(r'\w+\/\w+\/\w+', line) and not "checkVersion.j" in line and not "completeRegistration.j" in line and not "softwareUpdateAvailable.j" in line:
        #test = re.sub(r'(\.php$)|(\.jsp$)|(\.asp$)|(\.aspx$)', '.%EXT%', line)
        #test = re.sub(r'(\.asa$)|(\.cfm$)|(\.php$)|(\.jsp$)|(\.asp$)|(\.aspx$)', '.%EXT%', line)
        test = re.sub(r'(\.cfm$)|(\.php$)|(\.jsp$)|(\.asp$)|(\.aspx$)', '.%EXT%', line)
        print(test, end="")
        #fin.add(test)
    else:
        print(line, end="")
        #fin.add(line)


if not sys.stdin.isatty():
    input_stream = sys.stdin
    for line in input_stream:
        change(line)

else:
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    for line in lines:
        change(line)

#for i in fin:
    #print(i.strip())
