#Adds (time, label) pairs from file to plot
def annotate(plot, hist, file, div):
    #if not labely:
    #    labely = max(hist)
    for line in file:
        (x, label) = line.split(' ', 1)
        x = int(x)
        label = label.rstrip()
        y = hist[x/div]

        plot.annotate(label, xy=(x, y), xytext=(50, 60),
                      textcoords="offset points",
                      bbox=dict(boxstyle="round", fc="#d3d3d3", ec="#a8a8a8"),
                      arrowprops=dict(arrowstyle="fancy", fc="#d3d3d3",
                                      facecolor='purple', ec="#a8a8a8",
                                      connectionstyle="angle3,angleA=0,angleB=-90"))
