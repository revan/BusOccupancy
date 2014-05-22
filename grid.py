import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
from annotate import annotate

def addPacket(packet, addresses):
    for add in packet["adds"].values():
        if add not in addresses:
            addresses[add] = [packet["time"],packet["time"],1]
        else:
            addresses[add][1] = packet["time"]
            addresses[add][2] += 1

def makePlot(x,y,prefix):
    plot.gcf().set_size_inches(x,y)
    #plot.tight_layout()
    plot.savefig('img/' + prefix + '-grid-' +
                 str(x) + 'x' + str(y) + '.png', dpi=200)

def graphGrid(jason):
    PREFIX="prob"
    # Sets how many times we want to see a MAC before it's added to the graph.
    # Only active when PREFIX is set to "prob".
    COINCIDENCE = 0

    if PREFIX=="bus":
        annot = open('data/plot.labels')

    # Binsize in microseconds -- 1 is 1us, 1000 is 1ms, 100,000 is 0.1s, etc.
    BINSIZE = 100000

    xcoord = []
    ycoord = []
    macAddresses = {}

    #firstmSec = int(findTime.search(firstLine).group(1))/BINSIZE
    jason["packets"].apply(lambda row: addPacket(row, macAddresses), axis=1)

    lastSec = jason["packets"].tail(1)["time"].item()

    c25 = 0
    c50 = 0
    c75 = 0
    c100 = 0
    c125 = 0
    c150 = 0

    for value in macAddresses.values():
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
        print("Number of MACs within:")
        print(" * 25:  "+ str(c25))
        print(" * 50:  "+ str(c50))
        print(" * 75:  "+ str(c75))
        print(" * 100: "+ str(c100))
        print(" * 125: "+ str(c125))
        print(" * 150: "+ str(c150))

    plot.xlim(0,lastSec)
    plot.ylim(0,lastSec)
    plot.scatter(xcoord, ycoord)

    plot.title(PREFIX)
    plot.xlabel('Time first seen (microseconds since ' +
                jason["initial_time"] + ')')
    plot.ylabel('Time last seen (microseconds since ' +
                jason["initial_time"] + ')')

    if PREFIX=="bus":
        annotate(plot, annot, 10, xoff=10, yoff=-10, ymax = lastSec)
        annot.close()

    #makePlot(5,5)
    #makePlot(6,6)
    #makePlot(5.5,5)
    makePlot(6.5,6, PREFIX)
    makePlot(7.5,7, PREFIX)
    makePlot(8,7.5, PREFIX)

    plot.show()
