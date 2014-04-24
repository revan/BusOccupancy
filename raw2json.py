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

#findMac = re.compile(r"([\da-f]{2}(?:[-:][\da-f]{2}){5})")
findBSSID = re.compile(r"(BSSID:)([\da-f]{2}(?:[-:][\da-f]{2}){5})")
findDessert = re.compile(r"([DSRT]A:)([\da-f]{2}(?:[-:][\da-f]{2}){5})")
findTime = re.compile(r"(\d+)(us)")

for line in args.infile:
    time = findTime.search(line)
    print(time.group(1))
    for bssid in findBSSID.findall(line):
        # Flag all routers
        for mac in macs:
            if bssid[1]==mac["add"]:
                mac["r"]=1
                break
        else:
            macs.append({
                "add":bssid[1],
                "r":1,
                "num":output["num_macs"]
            })
            output["num_macs"]+=1
    if "BSSID" in line and "Broadcast" in line:
        # Even though we're keeping routers, Broadcast lines are still useless.
        continue
    for food in findDessert.findall(line):
        for mac in macs:
            if food[1]==mac["add"]:
                break
        else:
            macs.append({
                "add":food[1],
                "r":0,
                "num":output["num_macs"]
            })
            output["num_macs"]+=1
        ldic = {food[0][0]: food[1]}

print(macs)
args.infile.close()
args.outfile.close()
