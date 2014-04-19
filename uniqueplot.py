#!/bin/python
import numpy as np
import time as time
import matplotlib.pyplot as plot
from collections import defaultdict, Counter
import re
from annotate import annotate
file = open('data/plot.pcap')
annot = open('data/plot.labels')

findMac = re.compile("([0-9a-f]{2}:){5}([0-9a-f]{2})")
findTime = re.compile(" (\d+)us")

# Forced end time in whatever unit we're using -- see BINSIZE.
END_TIME = 1128
# Multiply together to get binsize. S is number of microseconds, L is for
# divisions greater than 1s -- BINSIZE_S should not be larger than 10^6.
BINSIZE_S = 1000000
BINSIZE_L = 2
BINSIZE = BINSIZE_S*BINSIZE_L

hist = []
bin = []

firstLine = file.readline()
firstmSec = int(findTime.search(firstLine).group(1))/BINSIZE
file.seek(0)
prevmSecond = -1

for i, line in enumerate(file):
	try:
		tim = int(findTime.search(line).group(1))/BINSIZE
		msec = tim - firstmSec

		if END_TIME > 0 and msec >= END_TIME:
			break

		if msec == prevmSecond:
			# still in same bin
			# get MACs from line, add new
			for mac in findMac.findall(line):
				if not mac in bin:
					bin.append(mac)
		else:
			# add count, make new bin
			while (msec - prevmSecond) > 1:
				prevmSecond+=1
				hist.append(0)
			prevmSecond = msec
			hist.append(len(bin))
			bin = []

	except IndexError:
		print i
	except AttributeError:
		print line


lastmSec = msec

file.close()

div = 1000000/BINSIZE_S

xaxis = [(BINSIZE_L*j)/div for j in range(len(hist))]

plot.bar(xaxis, hist, width = 1, edgecolor='#000033')
plot.xlim(0, BINSIZE_L*len(hist)/div)
plot.xlabel('Seconds since 1:51PM')
plot.ylabel('Unique MACs in 2 second interval')
plot.title('April 7th, A Route')

annotate(plot, hist, annot, BINSIZE_L)
annot.close()

def makePlot(x,y):
    plot.gcf().set_size_inches(x,y)
    #plot.tight_layout()
    plot.savefig('img/bus-unique-' +
                 str(x) + 'x' + str(y) + '.png', dpi=200)

#makePlot(12,6) #Cuts off a label.
makePlot(13,6)
makePlot(14,6)
makePlot(15,6)
makePlot(13,7)
makePlot(14,7)
makePlot(15,7)
makePlot(16,7)

plot.show()
