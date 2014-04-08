#!/bin/python
import numpy as np
import time as time
import matplotlib.pyplot as plot

file = open('H.pcap')

times = []

for i, line in enumerate(file):
	
	try:
		timeObject = time.strptime(line.split()[0].split('.')[0], '%H:%M:%S')
		if i == 0:
			first = timeObject
			firstSec = first.tm_sec+first.tm_min*60+first.tm_hour*3600
			firstMin = first.tm_min*60+first.tm_hour*3600


		times.append(timeObject)
	except IndexError:
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
plot.ylabel('Packets in 1 second interval')
plot.title('tcpdump -i wlp3s0 -e')


plot.annotate('Davidson', xy=(60, 500), xytext=(100, 900), arrowprops=dict(facecolor='red', shrink=0.05))
plot.annotate('ARC', xy=(240, 200), xytext=(300, 1500), arrowprops=dict(facecolor='red', shrink=0.05))
plot.annotate('HILL', xy=(360, 200), xytext=(450, 1500), arrowprops=dict(facecolor='red', shrink=0.05))
plot.annotate('Stadium Lot', xy=(540, 200), xytext=(600, 1500), arrowprops=dict(facecolor='red', shrink=0.05))
plot.annotate('bridge', xy=(600, 200), xytext=(600, 200))
plot.annotate('Student Center', xy=(900, 1200), xytext=(950, 1500), arrowprops=dict(facecolor='red', shrink=0.05))
plot.annotate('Scott', xy=(1140, 200), xytext=(1200, 1000), arrowprops=dict(facecolor='red', shrink=0.05))
plot.annotate('SAC', xy=(1380, 200), xytext=(1400, 900), arrowprops=dict(facecolor='red', shrink=0.05))

plot.savefig('packets.png')
plot.show()
