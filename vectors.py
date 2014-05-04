#Makes vectors of 1's between first and last sightings, sums vectors
# ./graph.py -t vectors -n f -s -50 -e 1816
import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import graphlib
from segments import readDelims

def addPacket(packet, addresses):
    for add in packet["adds"].values():
        if add not in addresses:
            addresses[add] = [packet["time"],packet["time"],1]
        else:
            addresses[add][1] = packet["time"]
            addresses[add][2] += 1

def plotVectors(json, coincidence=30, name="", labels=False):
    delims = readDelims()
    actual = []
    stopx = []
    for stop in delims:
        actual.append(stop['actual'])
        stopx.append(stop['start'])
    vectors = {}

    macAddresses = {}

    json["packets"].apply(lambda row: addPacket(row, macAddresses), axis=1)

    last = json["packets"]["time"].iget(-1)

    for key in macAddresses.keys():
        if (macAddresses[key][1] - macAddresses[key][0]) < coincidence:
            continue
        vectors[key] = np.zeros(last)
        vectors[key][macAddresses[key][0] : macAddresses[key][1]] = 1
        

    sum = np.zeros(last)
    for vector in vectors.values():
        sum += vector

    print(sum)
    print(int(last))

    plot.step(range(int(last)), sum.tolist())

    plot.xlabel('Seconds since start')
    plot.ylabel('Devices', color='b')

    ax2 = plot.twinx()
    ax2.step(stopx, actual, 'r', where="post")
    for t1 in ax2.get_yticklabels():
        t1.set_color('r')
    ax2.set_ylabel('Riders', color='r')

    plot.xlim(0, 1816)

    graphlib.makeWidePlot("bus", "vectors")

    if(labels):
        for stop in delims:
            graphlib.annotate(stop["name"], stop["start"], stop["actual"], 10,10)

    plot.show()