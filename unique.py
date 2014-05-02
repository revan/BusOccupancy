import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
from graphlib import makePlot, annotate

def addToBin(packet, bins, curBin, binsize):
    if int(packet["time"]) > curBin["time"]:
        curBin["time"] = int(packet["time"])
        curBin["addresses"] = set()
    for address in packet["adds"].values():
        if address not in curBin["addresses"]:
            bins[int(packet["time"]/binsize)]+=1
            curBin["addresses"].add(address)

def plotUnique(jason, binsize=1, labels=None):
    #annot = open('data/plot.labels')

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
    plot.title('April 7th, A Route')

    # annotate(plot, hist, annot, BINSIZE_L)
    # annot.close()

    makePlot(13,6, "bus", "unique")
    makePlot(14,6, "bus", "unique")
    makePlot(15,6, "bus", "unique")
    makePlot(13,7, "bus", "unique")
    makePlot(14,7, "bus", "unique")
    makePlot(15,7, "bus", "unique")
    makePlot(16,7, "bus", "unique")

    plot.show()
