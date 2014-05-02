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

def plotGrid(jason, coincidence=0, name="", labels=False):
    xcoord = []
    ycoord = []
    macAddresses = {}

    jason["packets"].apply(lambda row: addPacket(row, macAddresses), axis=1)

    last = jason["packets"]["time"].iget(-1)

    for value in macAddresses.values():
        if value[2] < coincidence:
            continue
        xcoord.append(value[0])
        ycoord.append(value[1])

    plot.xlim(0,last)
    plot.ylim(0,last)
    plot.scatter(xcoord, ycoord)

    if coincidence>0:
        plot.title(name + " -- under coincidence " + str(coincidence))
    else:
        plot.title(name)
    plot.xlabel('Time first seen (seconds since ' +
                jason["initial_time"] + ')')
    plot.ylabel('Time last seen (seconds since ' +
                jason["initial_time"] + ')')

    if(labels):
        graphlib.squareAnnotate(plot, ymax=last)

    graphlib.makeSquarePlot(name, "grid")

    plot.show()
