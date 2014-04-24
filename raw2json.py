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

first_line = args.infile.readline()
args.infile.seek(0)

macs = {}
output = {
    "initial_time": first_line[:15], # Fancy initial time (HH:MM:SS.xxxxxx)
    "routers": [],
    "num_macs": 0,
    "packets": []
}

findBSSID = re.compile(r"(BSSID:)([\da-f]{2}(?:[-:][\da-f]{2}){5})")
findDessert = re.compile(r"([DSRT]A:)([\da-f]{2}(?:[-:][\da-f]{2}){5})")
findTime = re.compile(r"(\d+)(us)")
findStrength = re.compile(r"(-)(\d+)(dB)")

first_time = findTime.search(first_line).group(1) # Initial time in microseconds

for line in args.infile:
    try:
        ldic = {
            "time": first_time - int(findTime.search(line).group(1)),
            "str": -1 * int(findStrength.search(line).group(2))
        }
    except AttributeError:
        ldic["str"] = None
    for bssid in findBSSID.findall(line):
        # Flag all routers
        if bssid[1] in macs:
            macs[bssid[1]]["r"]=1
            continue
        else:
            macs[bssid[1]] = {
                "num":output["num_macs"],
                "r":1
            }
            output["num_macs"]+=1
    if "BSSID" in line and "Broadcast" in line:
        # Even though we're keeping routers, Broadcast lines are still useless.
        continue
    for food in findDessert.findall(line):
        if food[1] not in macs:
            macs[food[1]] = {
                "num":output["num_macs"],
                "r":0
            }
            output["num_macs"]+=1
        ldic[food[0][0]] = food[1]
    output["packets"].append(ldic)


args.infile.close()
args.outfile.close()
