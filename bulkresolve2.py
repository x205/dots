#!/usr/bin/env python3

import argparse
import os
import sys
import dns.resolver
import asyncio
from dns.asyncresolver import Resolver
from colorama import Fore
from urllib.parse import urlparse


async def dns_query(args, domain, rtype = 'A'):

    # create an asyncio Resolver instance
    resolver = Resolver()

    # add resolvers
    if os.path.isfile(args.resolvers):
        with open(args.resolvers) as f:
            resolvers = [r.strip() for r in f.readlines() if r.strip() != ""]

    resolver.nameservers = resolvers

    # call and asynchronously await .resolve() to obtain the DNS results
    resolver: dns.resolver.Answer = await resolver.resolve(domain, rdtype=rtype)

    return domain, resolver

async def dns_bulk(args, *queries, **kwargs):
    ret_ex = kwargs.pop('return_exceptions', True)
    coros = [dns_query(args, domain) for domain in list(queries)]
    return await asyncio.gather(*coros, return_exceptions=ret_ex)


def get_host(line):
    parsed = urlparse(line)
    if parsed.scheme:
        host = parsed.netloc
    else:
        host = line.split('/')[0]
    return host


async def main(args):
    domains = set()
    tmpdomains = set()
    urldict = dict()
    exceptions = list()
    results = list()
    oos = list()

    # Get ips from file
    if os.path.isfile("ips"):
        with open("ips") as fh:
            ips = [i.strip() for i in fh.readlines()]
    elif os.path.isfile("../ips"):
        with open("../ips") as fh:
            ips = [i.strip() for i in fh.readlines()]
    else:
        print(Fore.LIGHTRED_EX + "[!] No ips file found" + Fore.RESET)
        sys.exit(1)

    if args.file and not args.url and args.file != '-':
        with open(args.file, "r") as f:
            lines = f.readlines()
            for line in lines:
                host = get_host(line)
                tmpdomains.add(host)

    elif args.url:
        tmpdomains.add(args.url)

    elif args.file == '-' or not sys.stdin.isatty():
        inp = sys.stdin
        for line in inp:
            line = line.strip()
            host = get_host(line)
            tmpdomains.add(host)

    res = await dns_bulk(args, *list(tmpdomains))


    exceptions = [i for i in res if isinstance(i, Exception)]
    results = [i for i in res if not isinstance(i, Exception)]

    if not args.hide_errors:
        for e in exceptions:
            if isinstance(e, dns.exception.DNSException):
                sys.stderr.write(f"DNS Error:{e.msg}\n")
            elif not args.only_dns:
                sys.stderr.write(f"Non DNS Error - {e}")



    for domain, answer in results:
        inflag = 0
        for ip in answer:
            ip = ip.to_text()
            if ip in ips:
                inflag = 1
                print(ip, domain)
            else:
                if inflag == 1:
                    print(f"{Fore.LIGHTRED_EX}[!!] {ip} {domain} is not in scope, "
                          f"but previous ip was [!]. slug: aonetwo{Fore.RESET}")
                else:
                    oos.append(domain)

    if args.show_oos:
        for out in oos:
            print(f"Out-Of-Scope: {out}")
                    


parser = argparse.ArgumentParser(description="Resolve bulk domain names and check if they're in scope")
parser.add_argument("-f", "--file",
                    help="File to read URLs from, '-' for stdin")
parser.add_argument("-u", "--url",
                    help="URL to lookup")
parser.add_argument("-r", "--resolvers",
                    help="File to read resolvers from, default is: $HOME/resolvers.txt", 
                    default="$HOME/resolvers.txt")
parser.add_argument("-s", "--show-oos",
                    help="Print out of scope domains", action="store_true")
parser.add_argument("-eh", "--hide-errors",
                    help="Don't print exceptions", action="store_true")
parser.add_argument("-eo", "--only-dns",
                    help="Print only DNS exceptions", action="store_true")

args = parser.parse_args()

asyncio.run(main(args))
