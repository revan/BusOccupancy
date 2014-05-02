import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import graphlib

def addToBin(packet, bins, curBin, binsize):
    if int(packet["time"]) > curBin["time"]:
        bins[int(curBin["time"]/binsize)] = len(curBin["addresses"])
        curBin["time"] = int(packet["time"])
        curBin["addresses"] = set()
    for address in packet["adds"].values():
        curBin["addresses"].add(address)

def plotUnique(jason, binsize=1, name="", labels=False):
    last = jason["packets"]["time"].iget(-1)
    bins = np.zeros(int(last/binsize)+1, np.int)

    curBin = {
        "time": 0,
        "addresses": set()
    }

    jason["packets"].apply(lambda row: addToBin(row, bins, curBin, binsize),
                           axis=1)

    xaxis = [j*binsize for j in range(len(bins))]
    plot.bar(xaxis, bins, width = 1, edgecolor='#000033')
    plot.xlim(0, last)
    plot.xlabel('Seconds since '+jason["initial_time"])
    plot.ylabel('Unique MACs in '+str(binsize)+' second interval')
    plot.title(name)

    if(labels):
        graphlib.wideAnnotate(plot, bins, binsize)

    graphlib.makeWidePlot("bus", "unique")

    plot.show()
