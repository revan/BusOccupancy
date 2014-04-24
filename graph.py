#!/bin/python3
import argparse
import json
from filter import filter

parser = argparse.ArgumentParser(prog='graph', description=
                                 'Create graphs from JSON created by raw2json')
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                    default='data/in.json',
                    help='Packet log in JSON format (defaults to data/in.json)')
args = parser.parse_args()

jason = json.load(args.infile)

filter(jason, routers=True)

args.infile.close()

print(jason)
