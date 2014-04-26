import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
from annotate import annotate

def addPacket(packet, addresses, units):
    for add in packet["adds"].values():
        if add not in addresses:
            addresses[add] = [packet["time"]/units,packet["time"]/units,1]
        else:
            addresses[add][1] = packet["time"]/units
            addresses[add][2] += 1

def makePlot(x,y,prefix):
    plot.gcf().set_size_inches(x,y)
    #plot.tight_layout()
    plot.savefig('img/' + prefix + '-grid-' +
                 str(x) + 'x' + str(y) + '.png', dpi=200)

def graphGrid(jason, coincidence=0, units=1, labels=None):
    PREFIX="prob"

    if PREFIX=="bus":
        annot = open('data/plot.labels')

    xcoord = []
    ycoord = []
    macAddresses = {}

    jason["packets"].apply(lambda row: addPacket(row, macAddresses, units),
                           axis=1)

    last = jason["packets"].tail(1)["time"].item()/units

    closeLims = [1,5,10,15,30,60,90,120]
    closeNums = [0,0,0,0,0,0,0,0,0]

    for value in macAddresses.values():
        if value[2] < coincidence:
            continue
        xcoord.append(value[0])
        ycoord.append(value[1])
        diff = value[1] - value[0]
        for i,lim in enumerate(closeLims):
            if diff < lim:
                closeNums[i] += 1

    if PREFIX=="prob":
        print("Number of MACs within:")
        for i,lim in enumerate(closeLims):
            print(" * "+str(lim)+": "+str(closeNums[i]))

    plot.xlim(0,last)
    plot.ylim(0,last)
    plot.scatter(xcoord, ycoord)

    if coincidence>0:
        plot.title(PREFIX + " -- under coincidence " + str(coincidence))
    else:
        plot.title(PREFIX)
    plot.xlabel('Time first seen (microseconds since ' +
                jason["initial_time"] + ')')
    plot.ylabel('Time last seen (microseconds since ' +
                jason["initial_time"] + ')')

    if PREFIX=="bus":
        annotate(plot, annot, 10, xoff=10, yoff=-10, ymax = last)
        annot.close()

    #makePlot(5,5)
    #makePlot(6,6)
    #makePlot(5.5,5)
    makePlot(6.5,6, PREFIX)
    makePlot(7.5,7, PREFIX)
    makePlot(8,7.5, PREFIX)

    plot.show()
