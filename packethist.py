import argparse
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
from graphlib import makePlot, annotate
from filter import filter

def addPacket(packet, addresses):
    for add in packet["adds"].values():
        if add not in addresses:
            addresses[add] = [packet["time"],packet["time"],1]
        else:
            addresses[add][1] = packet["time"]
            addresses[add][2] += 1


def plotPacketHistogram(jason, units=1000000, binsize=1, labels=None, endTime=0, coincidence=0):

    indices = []
    packetAxis = []
    macAddresses = {}
   
    jason["packets"]["time"] /= units
    jason["packets"].apply(lambda row: addPacket(row, macAddresses), axis=1)

    last = jason["packets"]["time"].iget(-1)
   
    i = 0
   
    for value in macAddresses.values():
        if value[2] < coincidence:
            continue
	  
        check = value[0]+last-value[1]
        
        if check < 120:
            indices.append(i)
            packetAxis.append(value[2])
            i += 1
     
    plot.bar(indices, packetAxis, color = "black", align = "center")
    plot.xlabel("Unique MAC addresses that stayed for entire class period")
    plot.ylabel('Number of Packets seen for each MAC address')
    plot.title('Packet Distribution of MAC addresses that remained the whole class period')
    
    plot.show()
     
     
   