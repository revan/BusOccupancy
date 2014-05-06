# Note: Filtering out strength/endTime does not properly update num_macs.
# This would be very difficult to implement. Not sure if we should do it.
# Note 2: Doing discrete loops for each function is apparently faster than a
# single loop, counterintuitively.
def filter(jason, rmRouters, strength, removeEmptyStr, endTime):
    routers = set(jason["routers"])
    # Filter Strength
    fil = jason["packets"]["str"].apply(lambda s: s > strength and
                                        (s!=0 or not removeEmptyStr))
    jason["packets"] = jason["packets"][fil]
    # Filter End Time
    if endTime>0:
        fil = jason["packets"]["time"].apply(lambda t: t<endTime)
        jason["packets"] = jason["packets"][fil]
    # Filter Routers
    if rmRouters:
        fil = jason["packets"]["adds"].apply(lambda macs:
                                             filterRouters(macs, routers))
        jason["packets"] = jason["packets"][fil]
        jason["num_macs"] -= len(jason["routers"])
        del jason["routers"]

# Returns False if the packet has no items left after routers have been removed.
def filterRouters(macs, routers):
    macs = dict((type,id) for type,id in macs.items() if id not in routers)
    return len(macs) != 0
