#!/bin/python3
import argparse
import json
from filter import filter
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(prog='graph', description=
                                 'Create graphs from JSON created by raw2json')
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                    default='data/in.json',
                    help='Packet log in JSON format (defaults to data/in.json)')
args = parser.parse_args()

jason = json.load(args.infile)

jason["packets"] = pd.DataFrame(jason["packets"])
jason["routers"] = np.array(jason["routers"])

filter(jason, rmRouters=True, strength=-60, removeEmptyStr=True)

args.infile.close()

print(jason)
