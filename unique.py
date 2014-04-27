import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
from graphlib import makePlot, annotate

def addToBin(time,bins,binsize):
    bins[int(time/binsize)]+=1

def plotUnique(jason, units=1000000, binsize=1, labels=None, endTime=0):
    #annot = open('data/plot.labels')

    hist = []
    jason["packets"]["time"] /= units
    last = jason["packets"]["time"].iget(-1)
    if endTime > 0:
        last = min(endTime,jason["packets"]["time"].iget(-1))
        fil = jason["packets"]["time"].apply(lambda t: t<endTime)
        jason["packets"] = jason["packets"][fil]
    bins = np.zeros(int(last/binsize)+1, np.int)
    jason["packets"]["time"].apply(lambda t: addToBin(t, bins, binsize))

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
