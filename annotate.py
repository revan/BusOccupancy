#Adds (time, label) pairs from file to plot
def annotate(plot, hist, file):
	labely = max(hist)
	for line in file:
		(x, label) = line.split(' ', 1)
		x = int(x)
		y = hist[x]

		plot.annotate(label, xy=(x, y), xytext=(x, labely), arrowprops=dict(facecolor='red', shrink=0.05))

