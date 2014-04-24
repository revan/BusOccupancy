def filter(jason, routers=False, strength=False, strlim=0,
           removeEmptyStr=False):
    routers = set(jason["routers"])
    removeArr = []
    for packet in jason["packets"]:
        removePkt = False
        if routers:
            removePkt = filterRouters(packet, routers)
        if strength:
            removePkt = removePkt or filterStrength(packet, strlim,
                                                    removeEmptyStr)
        if removePkt:
            removeArr.append(packet)
    for packet in removeArr:
        jason["packets"].remove(packet)
    if routers:
        del jason["routers"]

# Removes router addresses from each packet
# Returns True if a packet has no addresses attached to it
def filterRouters(packet, routers):
    remove=[]
    for type, add in packet["adds"].items():
        if add in routers:
            remove.append(type)
    for type in remove:
        del packet["adds"][type]
    if len(packet["adds"]) == 0:
        return True
    return False

# Returns True if a packet doesn't meet the strength limit
def filterStrength(packet, str, removeEmpty=False):
    if "str" in packet:
        if packet["str"] < str:
            return True
    elif removeEmpty:
        return True
    return False
