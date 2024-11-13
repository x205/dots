#!/usr/bin/env python3

import socket
import os
import sys
from urllib.parse import urlparse
from colorama import Fore


def getname(host):
    inflag = 0
    if os.path.isfile("ips"):
        with open("ips") as fh:
            ips = [i.strip() for i in fh.readlines()]
    elif os.path.isfile("../ips"):
        with open("../ips") as fh:
            ips = [i.strip() for i in fh.readlines()]
    else:
        print("[!] No ips file found")
        sys.exit(1)

    if host.startswith("http"):
        dname = urlparse(host).netloc
    else:
        dname = host.split('/')[0]
    dns = socket.getaddrinfo(dname, 443, family=socket.AF_INET)
    dnsips = set(i[4][0] for i in dns)

    for i in dnsips:
        if i in ips:
            print(i)
            inflag = 1
        else:
            if inflag == 1:
                print(f"{Fore.LIGHTRED_EX}[!!] {i} is not in scope, but previous ip was{Fore.RESET}")
    inflag = 0

if not sys.stdin.isatty(): 
    inp = sys.stdin
    for line in inp:
        line = line.strip()
        try:
            getname(line)
        except:
            print(f"Can't resolve {line}")
else:
    try:
        getname(sys.argv[1])
    except:
        print(f"Can't resolve {sys.argv[1]}")
