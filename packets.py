import numpy as np
import matplotlib.pyplot as plot
import graphlib


def addToBin(time, bins, binsize):
    bins[int(time/binsize)] += 1


def plotPackets(jason, binsize=1, labels=None):
    bins = np.zeros(int(jason["last"]/binsize)+1, np.int)
    jason["packets"]["time"].apply(lambda t: addToBin(t, bins, binsize))

    xaxis = [j*binsize for j in range(len(bins))]
    plot.bar(xaxis, bins, width=1, edgecolor='#000033')
    plot.xlim(0, jason["last"])
    plot.xlabel('Seconds since '+jason["initial_time"])
    plot.ylabel('Unique MACs in '+str(binsize)+' second interval')
    plot.title('April 7th, A Route')

    if(labels):
        graphlib.wideAnnotate(plot, bins, binsize)

    graphlib.makeWidePlot("bus", "packets")

    plot.show()
