import numpy as np
import pandas as pd

def filter(jason, rmRouters=False, strength=False, strlim=0,
           removeEmptyStr=False):
    addresses = jason["packets"]["adds"]
    routers = set(jason["routers"])
    if strength:
        suff = jason["packets"].apply(lambda row:
                                      filterStrength(row, strlim,
                                                     removeEmptyStr))
        jason["packets"] = jason["packets"][suff]
    if rmRouters:
        addresses = addresses.apply(lambda adds: filterRouters(adds,routers))
        jason["num_macs"] -= len(jason["routers"])
        del jason["routers"]
        nempty = jason["packets"].apply(lambda row: len(row["adds"])!=0,
                                        axis=1)
        jason["packets"] = jason["packets"][nempty]

# Removes router addresses from a given address dict.
def filterRouters(addresses, routers):
    remove = set()
    for type, add in addresses.items():
        if add in routers:
            remove.add(type)
    for type in remove:
        del addresses[type]

# Returns True if the strength is sufficient, False otherwise
def filterStrength(packet, str, removeEmpty=False):
    if "str" in packet:
        return packet["str"] > str
    return not removeEmpty
