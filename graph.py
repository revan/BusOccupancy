#!/bin/python3
import argparse
import json
import numpy as np
import pandas as pd
from filter import filter
from grid import graphGrid

parser = argparse.ArgumentParser(prog='graph', description=
                                 'Create graphs from JSON created by raw2json')
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                    default='data/in.json',
                    help='Packet log in JSON format (defaults to data/in.json)')
args = parser.parse_args()

jason = json.load(args.infile)

jason["packets"] = pd.DataFrame(jason["packets"])
jason["routers"] = np.array(jason["routers"])

# filter(jason, rmRouters=True, strength=-60, removeEmptyStr=True)
filter(jason, rmRouters=True)

args.infile.close()

graphGrid(jason)
