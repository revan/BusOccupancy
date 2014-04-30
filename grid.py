import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import graphlib

def addPacket(packet, addresses):
    for add in packet["adds"].values():
        if add not in addresses:
            addresses[add] = [packet["time"],packet["time"],1]
        else:
            addresses[add][1] = packet["time"]
            addresses[add][2] += 1

def plotGrid(jason, coincidence=0, units=1000000, labels=None):
    PREFIX="prob"

    if PREFIX=="bus":
        annot = open('data/plot.labels')

    xcoord = []
    ycoord = []
    macAddresses = {}

    jason["packets"]["time"] /= units
    jason["packets"].apply(lambda row: addPacket(row, macAddresses), axis=1)

    last = jason["packets"]["time"].iget(-1)

    closeLims = [1,5,10,15,30,60,90,120]
    closeNums = [0,0,0,0,0,0,0,0,0]

    for value in macAddresses.values():
        if value[2] < coincidence:
            continue
        xcoord.append(value[0])
        ycoord.append(value[1])
        diff = (value[0] + last) - value[1]
        for i,lim in enumerate(closeLims):
            if diff < lim:
                closeNums[i] += 1

    if PREFIX=="prob":
        print("Number of MACs within:")
        for i,lim in enumerate(closeLims):
            print(" * "+str(lim)+": "+str(closeNums[i]))
    print("Total MACs: "+str(len(xcoord)))

    plot.xlim(0,last)
    plot.ylim(0,last)
    plot.scatter(xcoord, ycoord)

    if coincidence>0:
        plot.title(PREFIX + " -- under coincidence " + str(coincidence))
    else:
        plot.title(PREFIX)
    plot.xlabel('Time first seen (seconds since ' +
                jason["initial_time"] + ')')
    plot.ylabel('Time last seen (seconds since ' +
                jason["initial_time"] + ')')

    if PREFIX=="bus":
        graphlib.annotate(plot, annot, 10, xoff=10, yoff=-10, ymax = last)
        annot.close()

    #graphlib.makePlot(6.5,6, PREFIX, "grid")
    #graphlib.makePlot(7.5,7, PREFIX, "grid")
    graphlib.makeSquarePlot(PREFIX, "grid")

    plot.show()
