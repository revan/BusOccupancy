#!/bin/python
import numpy as np
import time as time
import matplotlib.pyplot as plot
import re
from annotate import annotate

file = open('data/plot.pcap')
annot = open('data/plot.labels')

times = []

DB_CUTOFF = -40

for i, line in enumerate(file):
	try:
		timeObject = time.strptime(line.split()[0].split('.')[0], '%H:%M:%S')
		if i == 0:
			first = timeObject
			firstSec = first.tm_sec+first.tm_min*60+first.tm_hour*3600
			prevSec = firstSec
			firstMin = first.tm_min*60+first.tm_hour*3600

		dB = int(re.search("-\d+(?=dB)", line).group(0))
		if(dB > DB_CUTOFF):
			times.append(timeObject)
	except IndexError:
		pass
	except AttributeError:
		pass

else:
	last = timeObject
	lastSec = last.tm_sec+last.tm_min*60+last.tm_hour*3600
	lastMin = last.tm_min*60+last.tm_hour*3600
file.close()

secondsSince = [i.tm_sec+i.tm_min*60+i.tm_hour*3600 - firstSec for i in times]
(hist, bin_edges) = np.histogram(secondsSince, bins = range(lastMin-firstMin))

plot.bar(bin_edges[:-1], hist, width = 1)
plot.xlim(min(bin_edges), max(bin_edges))
plot.xlabel('Seconds since start')
plot.ylabel('Packets in 1 second interval, strength > '+str(DB_CUTOFF))
plot.title('tcpdump -i wlp3s0 -e')
plot.ylim(0, 100)


annotate(plot, hist, annot, labely=50)
annot.close()

plot.savefig('img/strength.png')
plot.show()
