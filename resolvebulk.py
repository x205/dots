#!/usr/bin/env python3

import argparse
import socket
import os
import sys
import dns.resolver
import asyncio
from dns.asyncresolver import Resolver
from colorama import Fore
from urllib.parse import urlparse
from typing import Tuple


async def dns_query(args, domain, rtype = 'A') -> dns.rrset.RRset:

    # create an asyncio Resolver instance
    resolver = Resolver()

    # add resolvers
    if os.path.isfile(args.resolvers):
        with open(args.resolvers) as f:
            resolvers = [r.strip() for r in f.readlines() if r.strip() != ""]
            with open("/etc/resolv.conf") as fh:
                sysresolvers = fh.read()
                if "1.1.1.1" in sysresolvers:
                    resolvers.append("1.1.1.1")
                if "8.8.8.8" in sysresolvers:
                    resolvers.append("8.8.8.8")

    resolver.nameservers = resolvers

    # call and asynchronously await .resolve() to obtain the DNS results
    resolver: dns.resolver.Answer = await resolver.resolve(domain, rdtype=rtype)

    return domain, resolver

async def dns_bulk(args, *queries: Tuple[str, str], **kwargs):
    ret_ex = kwargs.pop('return_exceptions', True)

    # Iterate over the queries and call (but don't await) the dns_query coroutine
    # with each query.
    # Without 'await', they won't properly execute until we await the coroutines
    # either individually, or in bulk using asyncio.gather
    coros = [dns_query(args, domain) for domain in list(queries)]

    # using asyncio.gather, we can effectively run all of the coroutines
    # in 'coros' at the same time, instead of awaiting them one-by-one.
    #
    # return_exceptions controls whether gather() should immediately 
    # fail and re-raise as soon as it detects an exception,
    # or whether it should just capture any exceptions, and simply
    # return them within the results.
    # 
    # return_exceptions is set to True,
    # which means if one or more of the queries fail, it'll simply
    # store the exceptions and continue running the remaining coros,
    # and return the exceptions inside of the tuple/list of results.
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

    #print(f"\n Sending {len(queries)} bulk queries\n")
    #res = await dns_bulk(*queries)
    #print(f"\n Got {len(res)} results\n\n")

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
                tmpdomains.add(line.strip())

    elif args.url:
        tmpdomains.add(args.url)

    elif args.file == '-' or not sys.stdin.isatty():
        inp = sys.stdin
        for line in inp:
            line = line.strip()
            tmpdomains.add(line)

    for d in tmpdomains:
        p = urlparse(d)
        host = get_host(d)

        if args.add_path:
            if not urldict.get(host) or urldict[host].count('&') > urldict[host].count('&'):
                urldict[host] = d
        if args.with_scheme:
            if not urldict.get(host):
                if p.scheme:
                    urldict[host] = p.scheme + "://" + p.netloc
                else:
                    urldict[host] = host
        else:
            if not urldict.get(host):
                urldict[host] = host


    res = await dns_bulk(args, *list(urldict.keys()))


    exceptions = [i for i in res if isinstance(i, Exception)]
    results = [i for i in res if not isinstance(i, Exception)]

    if not args.hide_errors:
        for e in exceptions:
            if isinstance(e, dns.exception.DNSException):
                sys.stderr.write(f"DNS Error:{e.msg.split(':')[-1].rstrip('.')}\n")
            elif not args.only_dns:
                sys.stderr.write(f"Non DNS Error - {e}")



    for domain, answer in results:
        inflag = 0
        for ip in answer:
            ip = ip.to_text()
            if ip in ips:
                inflag = 1
                if args.domain_only:
                    print(domain)
                elif args.ips_only:
                    print(ip)
                else:
                    print(ip, urldict[domain])
            else:
                if inflag == 1:
                    print(f"{Fore.LIGHTRED_EX}[!] {ip} {hostname} is not in scope, but previous ip was [!]{Fore.RESET}")
                    answer = input("Continue? > ")
                    if answer.lower().startswith('y'):
                        pass
                    else:
                        sys.exit(1)
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
                    help="File to read resolvers from, default is: ~/gitsbins/resolvers/resolvers.txt", 
                    default="~/resolvers/resolvers.txt")
parser.add_argument("-s", "--show-oos",
                    help="Print out of scope domains", action="store_true")
parser.add_argument("-eh", "--hide-errors",
                    help="Don't print exceptions", action="store_true")
parser.add_argument("-eo", "--only-dns",
                    help="Print only DNS exceptions", action="store_true")
parser.add_argument("-d", "--domain-only",
                    help="Print only domains", action="store_true")
parser.add_argument("-p", "--ips-only",
                    help="Print only ips", action="store_true")
parser.add_argument("-a", "--add-path",
                    help="Add path, scheme and query string to domain output", action="store_true")
parser.add_argument("-ws", "--with-scheme",
                    help="Add scheme to domain output", action="store_true")

args = parser.parse_args()

asyncio.run(main(args))
