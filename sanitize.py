#!/bin/python
import re

infile = open("data/plot.pcap")
outfile = open("data/clean.pcap", "w")

findMac = re.compile("([\da-f]{2}(?:[-:][\da-f]{2}){5})")
findBSSID = re.compile("(BSSID:)([\da-f]{2}(?:[-:][\da-f]{2}){5})")
findDA = re.compile("(DA:)([\da-f]{2}(?:[-:][\da-f]{2}){5})")
findRA = re.compile("(RA:)([\da-f]{2}(?:[-:][\da-f]{2}){5})")
findSA = re.compile("(SA:)([\da-f]{2}(?:[-:][\da-f]{2}){5})")
findTA = re.compile("(TA:)([\da-f]{2}(?:[-:][\da-f]{2}){5})")

delete_words=["Unknown)", "Unknown", "antenna", "ethertype", "(oui", "MHz",
              "11g", "Ethernet", "oui", "Command","nop","options","ctrl","Mb/s",
              "Flags", "IPv4", "00:00:00:00:00:00"]

for line in infile:
    if "BSSID" in line and "Broadcast" in line:
        continue
    for bssid in findBSSID.findall(line):
        line = line.replace(bssid[0], "")
        line = line.replace(bssid[1], "")
    for da in findDA.findall(line):
        line = line.replace(da[0], "")
    for ra in findDA.findall(line):
        line = line.replace(ra[0], "")
    for sa in findDA.findall(line):
        line = line.replace(sa[0], "")
    for ta in findDA.findall(line):
        line = line.replace(ta[0], "")
    for word in delete_words:
        line = line.replace(word, "")
    outfile.write(line)
infile.close()
outfile.close()
