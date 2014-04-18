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

END_TIME = 0
# Binsize in microseconds -- 1 is 1us, 1000 is 1ms, 100,000 is 0.1s, etc.
BINSIZE = 1000000

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


lastmSec = msec

file.close()

div = 1000000/BINSIZE

xaxis = [j/div for j in range(len(hist))]

plot.bar(xaxis, hist, width = 1)
plot.xlim(0, len(hist)/div)
plot.xlabel('Seconds since start')
plot.ylabel('Unique MACs in 0.1 second interval')
plot.title('tcpdump -i wlp3s0 -e')

annotate(plot, hist, annot)
annot.close()

plot.savefig('img/unique.png')
plot.show()
