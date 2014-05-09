import numpy as np
import matplotlib.pyplot as plot
import graphlib


class Binner:
    bins = None

    def __init__(self, binsize, last):
        self.time = 0
        self.macs = set()
        self.bins = np.zeros(int(last/binsize)+1, np.int)
        self.binsize = binsize

    def addPacket(self, packet):
        if int(packet["time"]) > self.time:
            self.bins[int(self.time/self.binsize)] = len(self.macs)
            self.time = int(packet["time"])
            self.macs = set(packet["adds"].values())
        else:
            self.macs.update(packet["adds"].values())


def plotUnique(jason, binsize=1, name="", labels=False):
    b = Binner(binsize, jason["last"])
    jason["packets"].apply(b.addPacket, axis=1)

    xaxis = [j*binsize for j in range(len(b.bins))]
    plot.bar(xaxis, b.bins, width=1, edgecolor='#000033')
    plot.xlim(0, jason["last"])
    plot.xlabel('Seconds since '+jason["initial_time"])
    plot.ylabel('Unique MACs in '+str(binsize)+' second interval')
    plot.title(name)

    if(labels):
        graphlib.wideAnnotate(plot, b.bins, binsize)

    graphlib.makeWidePlot("bus", "unique")

    plot.show()
