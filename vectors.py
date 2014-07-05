# Makes vectors of 1's between first and last sightings, sums vectors
# ./graph.py -t vectors -n f -s -50 -e 1816
import numpy as np
import matplotlib.pyplot as plot
from graphlib import annotate, makeWidePlot
from segments import readDelims
from grid import addPacket


def plotVectors(json, coincidence=0, name="", minTime=30, maxTime=1700,
                labels=False):
    delims = readDelims()

    macAddresses = {}
    json["packets"].apply(lambda row: addPacket(row, macAddresses), axis=1)

    sum = np.zeros(json["last"], dtype=np.int)
    for val in macAddresses.values():
        diff = val[1] - val[0]
        if ((diff > minTime) and (diff < maxTime) and (val[2] >= coincidence)):
            sum[val[0]: val[1]] += 1

    plot.xlabel('Seconds since start')
    plot.ylabel('Devices', color='b')
    plot.step(range(int(json["last"])), sum.tolist())

    actual = [stop['actual'] for stop in delims]
    stopx = [stop['start'] for stop in delims]
    ax2 = plot.twinx()
    ax2.step(stopx, actual, 'r', where="post")
    (t1.set_color for t1 in ax2.get_yticklabels())
    ax2.set_ylabel('Riders', color='r')
    plot.ylim(0, 30)
    plot.xlim(0, json["last"])

    if(labels):
        for stop in delims:
            annotate(stop["code"], stop["start"], stop["actual"], 10, 10)

    makeWidePlot("bus", "vectors")

    plot.show()
