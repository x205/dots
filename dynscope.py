#!/usr/bin/env python3

import argparse
import re
import sys
from urllib.parse import urlparse



def main():
    urls = []

    with open(args.regexfile, 'r') as fh:
        lines = fh.readlines()

    for line in lines:
        if line.startswith('http://') or line.startswith('https://'):
            clean_line = re.split('http[s]?://', line)[-1].split('?')[0].strip()
            clean_line = clean_line.rstrip('/')
            http = '^http://' + clean_line  + '/' + '.*'
            https = '^https://' + clean_line  + '/' + '.*'

            urls.append(http)
            urls.append(https)

        else:
            print('line doesnt start with http[s]?://')
            exit(1)
        

    regex = re.compile("|".join(urls))

    #if sys.stdin.isatty() and not args.file:
        #parser.error('No URLs specified')
    #if args.file == '-' or not args.file:
        #lines = sys.stdin.readlines()
    #else:
        #with open(args.file, 'r') as fh:
            #lines = fh.readlines()

    if sys.stdin.isatty() and not args.dynfile:
        parser.error('No dynfile specified')

    if args.dynfile == '-' or not args.dynfile:
        for url in sys.stdin.readlines():
            if re.match(regex, url.strip()):
                print(url.strip())
    else:
        with open(args.dynfile, 'r') as dynfile:
            for url in dynfile:
                if re.match(regex, url.strip()):
                    print(url.strip())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get in-scope urls from dyn url list')
    parser.add_argument('-r', '--regexfile', 
                        help='File to read in-scope URLs from')
    parser.add_argument('dynfile', nargs='?',
                        help='File to search for in-scope URLs')
    args = parser.parse_args()

    if not args.regexfile:
        parser.error('No regexfile specified')

    main()
