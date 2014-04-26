import numpy as np
import pandas as pd

# TODO: Add end time filtering

# Note: Filtering out strength does not properly update num_macs.
# This would be very difficult to implement. Not sure if we should do it.
def filter(jason, rmRouters=False, strength=0, removeEmptyStr=False):
    addresses = jason["packets"]["adds"]
    routers = set(jason["routers"])
    fil = jason["packets"].apply(lambda row:
                                 filterItem(row, strength, removeEmptyStr,
                                            rmRouters, routers), axis=1)
    jason["packets"] = jason["packets"][fil]
    if rmRouters:
        jason["num_macs"] -= len(jason["routers"])
        del jason["routers"]

def filterItem(packet, strength, removeEmptyStr, rmRouters, routers):
    if strength != 0 or removeEmptyStr:
        if not filterStrength(packet, strength, removeEmptyStr):
            return False
    if rmRouters:
        if not filterRouters(packet["adds"], routers):
            return False
    return True

# Removes router addresses from a given address dict.
def filterRouters(addresses, routers):
    remove = set()
    for type, add in addresses.items():
        if add in routers:
            remove.add(type)
    for type in remove:
        del addresses[type]

# Returns True if the strength is sufficient, False otherwise
def filterStrength(packet, str, removeEmpty):
    if "str" in packet:
        return packet["str"] > str
    return not removeEmpty
