import matplotlib.pyplot as plot
import graphlib


def addPacket(packet, addresses):
    for add in packet["adds"].values():
        if add not in addresses:
            addresses[add] = [packet["time"], packet["time"], 1, packet["str"]]
        else:
            addresses[add][1] = packet["time"]
            addresses[add][2] += 1
            addresses[add][3] += packet["str"]


def plotStrengthHistogram(jason, cutoff=120):
    macAddresses = {}
    jason["packets"].apply(lambda row: addPacket(row, macAddresses), axis=1)

    packetAxis = [val[3]/val[2] for val in macAddresses.values()
                  if (val[0]+jason["last"]-val[1]) < cutoff]

    xmax = len(packetAxis)
    plot.xlim(0, xmax)
    plot.bar(range(xmax), sorted(packetAxis), color="black")
    plot.xlabel("Unique MAC addresses present for the entire class period")
    plot.ylabel('Average Signal Strength for each MAC address')
    plot.title('April 7th, Classroom Signal Strength Distribution')

    graphlib.makeWidePlot("class", "strhist")
    plot.show()
