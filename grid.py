#!/bin/python
import numpy as np
import time as time
import matplotlib.pyplot as plot
from collections import defaultdict, Counter
import re
from annotate import annotate
from sys import argv


END_TIME = 0
PREFIX="bus"

# Sets how many times we want to see a MAC before it's added to the graph.
# Only active when PREFIX is set to "prob".
COINCIDENCE = 3

if PREFIX=="bus":
    annot = open('data/plot.labels')

findMAC = re.compile("([\da-f]{2}(?:[-:][\da-f]{2}){5})")
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
        if END_TIME > 0 and msec > END_TIME:
            break

        for mac in findMAC.findall(line):
            #print mac
            if mac == "00:00:00:00:00:00":
                #print "why does this keep happening"
                continue
            if "BSSID" in mac:
                #print "It's a router, I think"
                continue
            if mac not in macAddresses:
                #print "It's a new one"
                macAddresses[mac] = [msec, msec, 1]
            else:
                macAddresses[mac][1] = msec
                macAddresses[mac][2] += 1
    except IndexError:
        print i

lastSec = msec
file.close()

c25 = 0
c50 = 0
c75 = 0
c100 = 0
c125 = 0
c150 = 0

for value in macAddresses.itervalues():
    if value[2] < COINCIDENCE and PREFIX=="prob":
        continue
    xcoord.append(value[0])
    ycoord.append(value[1])
    diff = value[1] - value[0]
    if diff < 25:
        c25+=1
    if diff < 50:
        c50+=1
    if diff < 75:
        c75+=1
    if diff < 100:
        c100+=1
    if diff < 125:
        c125+=1
    if diff < 150:
        c150+=1

if PREFIX=="prob":
    print "Number of MACs within:"
    print " * 25:  "+ str(c25)
    print " * 50:  "+ str(c50)
    print " * 75:  "+ str(c75)
    print " * 100: "+ str(c100)
    print " * 125: "+ str(c125)
    print " * 150: "+ str(c150)

plot.xlim(0,lastSec)
plot.ylim(0,lastSec)
plot.scatter(xcoord, ycoord)

if PREFIX=="prob":
    plot.title('April 7th, Classroom')
if PREFIX=="bus":
    plot.title('April 7th, A Route')
plot.xlabel('Time first seen (0.1s)')
plot.ylabel('Time last seen (0.1s)')

if PREFIX=="bus":
    annotate(plot, annot, 10, xoff=10, yoff=-10, ymax = lastSec)
    annot.close()

def makePlot(x,y):
    plot.gcf().set_size_inches(x,y)
    #plot.tight_layout()
    plot.savefig('img/' + PREFIX + '-grid-' +
                 str(x) + 'x' + str(y) + '.png', dpi=200)

#makePlot(5,5)
#makePlot(6,6)
#makePlot(5.5,5)
makePlot(6.5,6)
makePlot(7.5,7)
makePlot(8,7.5)

plot.show()
