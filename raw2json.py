#!/bin/python3
import re
import argparse
import sys

parser = argparse.ArgumentParser(prog='raw2json', description=
                                 'Produce a JSON from raw tcpdump output.')
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                    default='data/in.dat',
                    help="Tcpdump output file (defaults to data/in.dat)")
parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout, help="Output file (defaults to stdout)")
args = parser.parse_args()

macs = []
output = {
    "initial_time": None,
    "routers": [],
    "num_macs": 0,
    "packets": []
}

findMac = re.compile("([\da-f]{2}(?:[-:][\da-f]{2}){5})")
findBSSID = re.compile("(BSSID:)([\da-f]{2}(?:[-:][\da-f]{2}){5})")
findDessert = re.compile("([DSRT]A:)([\da-f]{2}(?:[-:][\da-f]{2}){5})")

for line in args.infile:
    if "BSSID" in line and "Broadcast" in line:
        # Even though we're keeping routers, Broadcast lines are still useless.
        continue
    for bssid in findBSSID.findall(line):
        break
        # Flag all routers
    for food in findDessert.findall(line):
        ldic = {food[0][0]: food[1]}
args.infile.close()
args.outfile.close()
