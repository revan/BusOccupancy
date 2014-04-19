#!/bin/python
import numpy as np
import time as time
import matplotlib.pyplot as plot
from collections import defaultdict, Counter
import re
from annotate import annotate
from sys import argv

findMac = re.compile("([0-9a-f]{2}:){5}([0-9a-f]{2})")
findTime = re.compile(" (\d+)us")

# Binsize in microseconds -- 1 is 1us, 1000 is 1ms, 100,000 is 0.1s, etc.
BINSIZE = 100000

script, filename = argv
file = open(filename)

xcoord = []
ycoord = []
macAddresses = {}

firstLine = file.readline()
firstmSec = int(findTime.search(firstLine).group(1))/BINSIZE
file.seek(0)

for i, line in enumerate(file):
    try:
        tim = int(findTime.search(line).group(1))/BINSIZE
        msec = tim - firstmSec

        for mac in findMac.findall(line):
            if "BSSID" in mac:
                #print "It's a router, I think"
                continue
            if mac not in macAddresses:
                #print "It's a new one"
                macAddresses[mac] = [msec, msec]
            else:
                macAddresses[mac][1] = msec

    except IndexError:
        print i

else:
    lastSec = msec
file.close()

goodcount = 0
for value in macAddresses.itervalues():
    xcoord.append(value[0])
    ycoord.append(value[1])
    if (value[1] - value[0]) < 250:
        goodcount+=1

print "Number of MACs within acceptable range: " + str(goodcount)
plot.xlim(0,lastSec)
plot.ylim(0,lastSec)
plot.scatter(xcoord, ycoord)

plot.savefig('img/grid.png')
plot.show()
