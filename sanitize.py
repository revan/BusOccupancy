#!/bin/python
import re

infile = open("data/plot.pcap")
outfile = open("data/clean.pcap", "w")

findTime = re.compile(" (\d+)us")

delete_words=["Unknown)", "Unknown", "antenna", "ethertype", "(oui", "MHz",
              "11g", "Ethernet", "oui", "Command","nop","options","ctrl","Mb/s",
              "Flags", "IPv4"]

for line in infile:
    if "BSSID" in line and "Broadcast" in line:
        continue
    for word in delete_words:
        line = line.replace(word, "")
    outfile.write(line)
infile.close()
outfile.close()
