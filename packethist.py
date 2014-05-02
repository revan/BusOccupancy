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

def plotPacketHistogram(jason, labels=None, coincidence=0):
    packetAxis = []
    macAddresses = {}

    jason["packets"].apply(lambda row: addPacket(row, macAddresses), axis=1)

    last = jason["packets"]["time"].iget(-1)

    for value in macAddresses.values():
        if value[2] < coincidence:
            continue

        diff = value[0]+last-value[1]

        if diff < 120:
            packetAxis.append(value[2])

    plot.xlim(0,len(packetAxis));
    plot.bar(range(len(packetAxis)), packetAxis, color="black", align="center")
    plot.xlabel("Unique MAC addresses present for the entire class period")
    plot.ylabel('Number of Packets seen for each MAC address')
    plot.title('Packet Distribution for MAC addresses that remained the whole class period')

    graphlib.makeWidePlot("class","packethist")
    plot.show()
