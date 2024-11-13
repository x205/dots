#!/usr/bin/env python3

import argparse
import html
import os
import pathlib
import re
import sys
from urllib.parse import urlparse

urldict = {}
noparams = set()

extensions = {
        '.js', 'svg', '.css', '.jpg', '.jpeg', '.png', '.woff', '.woff2', 
        '.eot', '.ttf', '.gif', '.ico',
        } 

def geturls(args):
    if args.file == '-' or not args.file:
        lines = sys.stdin.readlines()

    else:
        with open(args.file, 'r') as fh:
            lines = fh.readlines()

    for line in lines:
        parsed = urlparse(line)

        if ':80' in line or ':443' in line:
            line = re.sub(':80|:443', "", line)
        if "http://" in line and not args.keep:
            line = re.sub("http://", "https://", line)
        if '&amp;' in line or '&quot;' in line:
            line = html.unescape(line)

        #ext = os.path.splitext(parsed.path)[-1].strip()
        ext = pathlib.Path(parsed.path).suffix.strip()

        if ext not in extensions or ext == '' or parsed.path.strip()[-1] == '/':
            if '?' in line and '=' in line:
                urlparams = line.split('?')
                url = urlparams[0]
                params = urlparams[1]

                if 'utm_' in params:
                    params = re.sub('utm_[a-z]+=[^&]*&', "", params)
                    if 'utm_' in params and params.count('=') == 1 and '&' not in params:
                        params = re.sub('utm_[a-z]+=[^&]*(&|$)', "", params)

                if not urldict.get(url) or urldict[url].count('&') < params.count('&'):
                    urldict[url] = params
            else:
                noparams.add(line)

    if args.all == True:
        for i in urldict:
            print(i + '?' + urldict[i], end="")
        for i in noparams:
            print(i, end="")

    if args.params == True:
        for i in urldict:
            print(i + '?' + urldict[i], end="")

    if args.noparams == True:
        for i in noparams:
            print(i, end="")


parser = argparse.ArgumentParser(description='Find unique URLs with/without parameters')
parser.add_argument('-p', '--params', 
                    help="Find unique URLs with parameters", action="store_true")
parser.add_argument('-n', '--noparams',
                    help="Find unique URLs without parameters", action="store_true")
parser.add_argument('-a', '--all',
                    help="Find all unique URLs", action="store_true")
parser.add_argument('-f', '--file',
                    help="File to read URLs from")
parser.add_argument('-k', '--keep', action="store_true",
                    help="Don't change http to https")

args = parser.parse_args()

if args.params == False and args.noparams == False and args.all == False:
    args.all = True

geturls(args)
