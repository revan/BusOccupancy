#!/bin/python
import numpy as np
import time as time
import matplotlib.pyplot as plot
from collections import defaultdict, Counter
import re
from annotate import annotate
file = open('data/plot.pcap')
annot = open('data/plot.labels')

hist = []
bin = []
prevSecond = 0
for i, line in enumerate(file):
	try:
		timeObject = time.strptime(line.split()[0].split('.')[0], '%H:%M:%S')
		if i == 0:
			first = timeObject
			firstSec = first.tm_sec+first.tm_min*60+first.tm_hour*3600
			firstMin = first.tm_min*60+first.tm_hour*3600

		second = timeObject.tm_sec+timeObject.tm_min*60+timeObject.tm_hour*3600
		minute = timeObject.tm_min*60+timeObject.tm_hour*3600

		if second == prevSecond:
			#still in same bin
			#get MACs from line, add new

			for mac in re.findall("([0-9a-f]{2}:){5}([0-9a-f]{2})", line):
				if not mac in bin:
					bin.append(mac)
		else:
			#add count, make new bin
			prevSecond = second
			hist.append(len(bin))
			bin = []

	except IndexError:
		print i

else:
	last = timeObject
	lastSec = second
	lastMin = minute
	
file.close()

bin_edges = range(1+lastSec-firstSec)

plot.bar(bin_edges[:-1], hist, width = 1)
plot.xlim(min(bin_edges), max(bin_edges))
plot.xlabel('Seconds since start')
plot.ylabel('Unique MACs in 1 second interval')
plot.title('tcpdump -i wlp3s0 -e')

annotate(plot, hist, annot)
annot.close()

plot.savefig('img/unique.png')
plot.show()