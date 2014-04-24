def filter(jason, routers=False, strength=False, strlim=0,
           removeEmptyStr=False):
    for packet in jason["packets"]:
        if routers:
            filterRouters(packet, jason["packets"], jason["routers"])
        if strength:
            filterStrength(packet, jason["packets"], strlim, removeEmptyStr)
    if routers:
        del jason["routers"]

def filterRouters(packet, packets, routers):
    for type, add in packet["adds"].item():
        if add in routers:
            del packet[type]
    if len(packet["adds"]) == 0:
        del packets.remove(packet)

def filterStrength(packet, packets, str, removeEmpty=False):
    if "str" in packet:
        if packet["str"] < str:
            packets.remove(packet)
    elif removeEmpty:
        packets.remove(packet)
