#!/usr/bin/env python3

import socket
import os
import sys
from urllib.parse import urlparse


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
    if host.startswith("http"):
        dname = urlparse(host).netloc
    else:
        dname = host.split('/')[0]
    dns = socket.getaddrinfo(dname, 443, family=socket.AF_INET)
    dnsips = set(i[4][0] for i in dns)

    for i in dnsips:
        if i in ips:
            print(i, host)
            inflag = 1
        else:
            if inflag == 1:
                print(f"[!] {i} {host} is not in scope, but previous ip was [!]")
    inflag = 0

if not sys.stdin.isatty(): 
    inp = sys.stdin
    for line in inp:
        line = line.strip()
        try:
            getname(line)
        except socket.gaierror as e:
            continue
        except Exception as e:
            print(f"[!] Error: {e}")
else:
    try:
        getname(sys.argv[1])
    except socket.gaierror as e:
        print(e)
        print(f"Can't resolve {sys.argv[1]}")
    except Exception as e:
        print(f"[!] Error: {e}")
