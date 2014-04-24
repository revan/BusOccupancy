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
    if "D" in packet:
        if packet["D"] in routers:
            del packet["D"]
    if "S" in packet:
        if packet["S"] in routers:
            del packet["S"]
    if "R" in packet:
        if packet["R"] in routers:
            del packet["R"]
    if "T" in packet:
        if packet["T"] in routers:
            del packet["T"]
    if not any(k in packet for k in ("D","S","R","T")):
        packets.remove(packet)

def filterStrength(packet, packets, str, removeEmpty=False):
    if "str" in packet:
        if packet["str"] < str:
            packets.remove(packet)
    elif removeEmpty:
        packets.remove(packet)
