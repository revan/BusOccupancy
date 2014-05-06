import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import graphlib
from grid import addPacket

def plotPacketHistogram(jason, cutoff=120):
    macAddresses = {}
    jason["packets"].apply(lambda row: addPacket(row, macAddresses), axis=1)

    packetAxis = [val[2] for val in macAddresses.values()
                  if (val[0]+jason["last"]-val[1]) < cutoff]

    xmax = len(packetAxis)
    plot.xlim(0,xmax)
    plot.yscale('log')
    plot.bar(range(xmax), sorted(packetAxis), color="black", log=True)
    plot.xlabel("Unique MAC addresses present for the entire class period")
    plot.ylabel('Number of Packets seen for each MAC address')
    plot.title('April 7th, Classroom Packet Distribution')

    graphlib.makeWidePlot("class","packethist")
    plot.show()
