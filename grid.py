#!/bin/python
import numpy as np
import time as time
import matplotlib.pyplot as plot
from collections import defaultdict, Counter
import re
from annotate import annotate
from sys import argv

script, filename = argv
file = open(filename)

xcoord = []
ycoord = []
macAddresses = {}
prevSecond = 0

for i, line in enumerate(file):
    try:
        timeObject = time.strptime(line.split()[0].split('.')[0], '%H:%M:%S')
        if i == 0:
            first = timeObject
            firstSec = first.tm_sec+first.tm_min*60+first.tm_hour*3600
            firstMin = first.tm_min*60+first.tm_hour*3600

        second = timeObject.tm_sec+timeObject.tm_min*60+timeObject.tm_hour*3600
        minute = timeObject.tm_min*60+timeObject.tm_hour*3600

        #if second == prevSecond:
            #still in same bin
            #get MACs from line, add new

        for mac in re.findall("([0-9a-f]{2}:){5}([0-9a-f]{2})", line):
            if mac not in macAddresses:
                tempList = []
                tempList.append(second)
                macAddresses[mac] = tempList
            else:
                macAddresses[mac].append(second)
        else:
            prevSecond = second

    except IndexError:
        print i

else:
    last = timeObject
    lastSec = second
    lastMin = minute
file.close()

for value in macAddresses.itervalues():
    xcoord.append(value[0])
    if len(value) == 1:
        ycoord.append(value[0])
    else:  
        ycoord.append(value[-1])
plot.scatter(xcoord, ycoord)
plot.show()
