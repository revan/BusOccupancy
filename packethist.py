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

def plotPacketHistogram(jason):
    macAddresses = {}
    jason["packets"].apply(lambda row: addPacket(row, macAddresses), axis=1)

    last = jason["packets"]["time"].iget(-1)

    packetAxis = [val[2] for val in macAddresses.values()
                  if val[0]+last-val[1] < 120]

    xmax = len(packetAxis)
    plot.xlim(0,xmax)
    plot.yscale('log')
    plot.bar(range(xmax), sorted(packetAxis), color="black",
             align="center",log=True)
    plot.xlabel("Unique MAC addresses present for the entire class period")
    plot.ylabel('Number of Packets seen for each MAC address')
    plot.title('April 7th, Classroom Packet Distribution')

    graphlib.makeWidePlot("class","packethist")
    plot.show()
