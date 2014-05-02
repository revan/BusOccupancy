import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import graphlib
import json
from itertools import combinations

def readDelims(file='data/sched.json'):
    phil = open(file)
    jason = json.load(phil)
    phil.close()
    for stop in jason:
        stop["uniques"] = set()
    return jason

def plotSegments(jason, name="", labels=False):
    # read delimeters for each stop
    delims = readDelims()

    x = []
    realy = []
    stopAdds = []
    for stop in delims:
        realy.append(stop['actual'])
        x.append(stop['start'])
        stopPackets = jason['packets']['time'].apply(lambda t: t>stop['start']
                                                    and t<stop['end'])
        currStopBin = set()
        jason['packets']['adds'][stopPackets].apply(
            lambda adds: currStopBin.update(adds.values()))
        stopAdds.append(currStopBin)

    intersectBins = [set() for i in range(len(x))]
    combobs = combinations(range(len(x)), 2)
    for combob in combobs:
        #if(combob[1]-combob[0] > len(x)-4):
        #    continue
        curSect = stopAdds[combob[0]].intersection(stopAdds[combob[1]])
        for i in range(combob[0],combob[1]):
            intersectBins[i+1].update(curSect)
    probably_junk = stopAdds[0].intersection(stopAdds[-1])

    y = np.zeros(len(x), np.int)
    for i,bin in enumerate(intersectBins):
        y[i] = len(bin - probably_junk) + 2
    y[0] = y[1] # For labelling purposes

    plot.xlabel('Seconds since '+jason["initial_time"])
    plot.ylabel('Number of bus occupants (predicted)')
    plot.xlim(0,delims[-1]['end'])
    plot.title(name)
    plot.step(x, y)
    plot.step(x, realy, color="purple", where="post")

    xy = zip(x,y)
    if(labels):
        for stop in delims:
            graphlib.annotate(stop["name"], stop["start"], stop["actual"], 10,10)

    graphlib.makeWidePlot("bus", "segments")

    plot.show()
