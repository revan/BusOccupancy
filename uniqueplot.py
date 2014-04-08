#!/bin/python
import numpy as np
import time as time
import matplotlib.pyplot as plot
from collections import defaultdict, Counter
import re
file = open('H.pcap')

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

print len(hist)

plot.bar(bin_edges[:-1], hist, width = 1)
plot.xlim(min(bin_edges), max(bin_edges))
plot.xlabel('Seconds since start')
plot.ylabel('Unique MACs in 1 second interval')
plot.title('tcpdump -i wlp3s0 -e')

plot.annotate('Davidson', xy=(60, 100), xytext=(60, 130), arrowprops=dict(facecolor='red', shrink=0.05))
plot.annotate('ARC', xy=(240, 120), xytext=(240, 135), arrowprops=dict(facecolor='red', shrink=0.05))
plot.annotate('HILL', xy=(360, 120), xytext=(360, 130), arrowprops=dict(facecolor='red', shrink=0.05))
plot.annotate('Stadium Lot', xy=(540, 30), xytext=(540, 40), arrowprops=dict(facecolor='red', shrink=0.05))
plot.annotate('bridge', xy=(600, 20), xytext=(600, 20))
plot.annotate('Student Center', xy=(900, 100), xytext=(900, 120), arrowprops=dict(facecolor='red', shrink=0.05))
plot.annotate('Scott', xy=(1140, 100), xytext=(1140, 110), arrowprops=dict(facecolor='red', shrink=0.05))
plot.annotate('SAC', xy=(1380, 100), xytext=(1380, 110), arrowprops=dict(facecolor='red', shrink=0.05))

plot.savefig('unique.png')
plot.show()