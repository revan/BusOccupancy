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
    macs = {}
    jason["packets"].apply(lambda row: addPacket(row, macs), axis=1)

    xcoord = [val[0] for val in macs.values() if val[2] > coincidence]
    ycoord = [val[1] for val in macs.values() if val[2] > coincidence]

    plot.xlim(0, jason["last"])
    plot.ylim(0, jason["last"])
    plot.scatter(xcoord, ycoord)

    if coincidence>0:
        name += " -- under coincidence " + str(coincidence)
    plot.title(name)
    plot.xlabel('Time first seen (seconds since ' + jason["initial_time"] + ')')
    plot.ylabel('Time last seen (seconds since ' + jason["initial_time"] + ')')

    if(labels):
        graphlib.squareAnnotate(plot, ymax=jason["last"])
    graphlib.makeSquarePlot(name, "grid")
    plot.show()
