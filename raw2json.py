#!/bin/python3
import re
from argparse import ArgumentParser, FileType
import sys
import json

parser = ArgumentParser(prog='raw2json',
                        description='Produce a JSON from raw tcpdump output.')
parser.add_argument('infile', nargs='?', type=FileType('r'),
                    default='data/in.dat',
                    help="Tcpdump output file (defaults to data/in.dat)")
parser.add_argument('outfile', nargs='?', type=FileType('w'),
                    default=sys.stdout,
                    help="Output file (defaults to stdout)")
args = parser.parse_args()

# Get the first line so we can get the time from the first packet, then rewind.
first_line = args.infile.readline()
args.infile.seek(0)

macs = {}
output = {
    "initial_time": first_line[:15],  # Fancy initial time (HH:MM:SS.xxxxxx)
    "routers": [],
    "num_macs": 0,
    "packets": []
}

findBSSID = re.compile(r"(BSSID:)([\da-f]{2}(?:[-:][\da-f]{2}){5})")
findDessert = re.compile(r"([DSRT]A:)([\da-f]{2}(?:[-:][\da-f]{2}){5})")
findTime = re.compile(r"(\d+)(us)")
findStrength = re.compile(r"(-)(\d+)(dB)")

# Initial time in microseconds
first_time = int(findTime.search(first_line).group(1))

for line in args.infile:
    for bssid in findBSSID.findall(line):
        # Flag all routers
        if bssid[1] in macs:
            macs[bssid[1]]["r"] = True
            continue
        else:
            macs[bssid[1]] = {
                "num": output["num_macs"],
                "r": True
            }
            output["num_macs"] += 1
    if "BSSID" in line and "Broadcast" in line:
        # Even though we're keeping routers, Broadcast lines are still useless.
        continue
    try:
        ldic = {
            "time": int(findTime.search(line).group(1)) - first_time,
            "adds": {}
        }
    except AttributeError:
        continue
    for food in findDessert.findall(line):
        if food[1] not in macs:
            macs[food[1]] = {
                "num": output["num_macs"],
                "r": False
            }
            ldic["adds"][food[0][0]] = output["num_macs"]
            output["num_macs"] += 1
        else:
            ldic["adds"][food[0][0]] = macs[food[1]]["num"]
    try:
        strength = -1 * int(findStrength.search(line).group(2))
        ldic["str"] = strength
    except AttributeError:
        # Some packets don't have a strength field.
        ldic["str"] = 0
    output["packets"].append(ldic)

output["routers"] = sorted(add["num"] for add in macs.values() if add["r"])

args.outfile.write(json.dumps(output))

args.infile.close()
args.outfile.close()
