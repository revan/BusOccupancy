import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import graphlib

def readDelims(file='data/delims.txt'):
    delims = []
    with open(file) as f:
        for line in f:
            s = line.split()
            delims.append({
                "start":int(s[0]),
                "end":int(s[1]),
                "name":s[2],
                "uniques": set()
                })
    return delims

def addToBins(packet, delims, currStop):
    #we're after the last stop
    if currStop[0] >= len(delims):
        return

    if packet['time'] > delims[currStop[0]]['end']:
        currStop[0]+=1
    if packet['time'] < delims[currStop[0]]['start']:
        return

    # add addresses to collection
    for address in packet['adds'].values():
        #if address not in delims[currStop[0]]['uniques']:
        delims[currStop[0]]['uniques'].add(address)

def plotSegments(json, labels=None):
    # read delimeters for each stop
    delims = readDelims()

    #Get the number of addresses in each range
    currStop = [0] #a list, because we need to pass by reference. ಠ_ಠ
    json['packets'].apply(lambda row: addToBins(row, delims, currStop), axis=1)

    #Find the intersect of each pair of consecutive stops
    x=[]
    y=[]
    for currStop in range(0,len(delims)-2):
        x.append(delims[currStop]['start'])
        y.append(len(delims[currStop]['uniques'].intersection(
            delims[currStop+1]['uniques'])))

    plot.step(x, y)

    graphlib.makeWidePlot("bus", "segments")

    plot.show()
