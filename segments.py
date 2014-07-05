import matplotlib.pyplot as plot
from graphlib import annotate, makeWidePlot
import json
from itertools import combinations


def readDelims(filename='data/sched.json'):
    phil = open(filename)
    jason = json.load(phil)
    phil.close()
    for stop in jason:
        stop["uniques"] = set()
    return jason


def getStopSet(packets, stop):
    curr = set()
    fil = packets['time'].apply(lambda t: t > stop['start'] and
                                t < stop['end'])
    packets['adds'][fil].apply(lambda adds: curr.update(adds.values()))
    return curr


def plotSegments(jason, name="", labels=False):
    # read delimeters for each stop
    delims = readDelims()

    stopAdds = [getStopSet(jason["packets"], stop) for stop in delims]
    intersectBins = [set() for stop in delims]
    combobs = combinations(range(len(delims)), 2)
    for combob in combobs:
        curSect = stopAdds[combob[0]].intersection(stopAdds[combob[1]])
        for i in range(combob[0], combob[1]):
            intersectBins[i+1].update(curSect)
    probably_junk = stopAdds[0].intersection(stopAdds[-1])

    y = [len(bin - probably_junk) + 2 for bin in intersectBins]
    y[0] = y[1]  # For labelling purposes

    x = [stop['start'] for stop in delims]
    realy = [stop['actual'] for stop in delims]
    plot.xlabel('Seconds since '+jason["initial_time"])
    plot.ylabel('Number of bus occupants (predicted)')
    plot.xlim(0, delims[-1]['end'])
    plot.title(name)
    plot.step(x, y)
    plot.step(x, realy, color="purple", where="post")

    if(labels):
        for stop in delims:
            annotate(stop["code"], stop["start"], stop["actual"], 10, 10)

    makeWidePlot("bus", "segments")

    plot.show()
