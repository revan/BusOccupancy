import matplotlib.pyplot as plot

#Adds (time, label) pairs from file to plot
def annotate(plot, file, mod, xoff=50, yoff=60, hist=None, ymax=0):
    for line in file:
        (x, label) = line.split(' ', 1)
        x = int(x)
        label = label.rstrip()
        if hist is None:
            y = mod*x
            x *=mod
            plot.plot([0,y],[x,y],'purple',linewidth=1)
            plot.plot([x,y],[x,ymax],'purple',linewidth=1)
        else:
            y = hist[x/mod]

        plot.annotate(label, xy=(x, y), xytext=(xoff, yoff),
                      textcoords="offset points",
                      bbox=dict(boxstyle="round", fc="#d3d3d3", ec="#a8a8a8"),
                      arrowprops=dict(arrowstyle="fancy", fc="#d3d3d3",
                                      ec="#a8a8a8", connectionstyle=
                                      "angle3,angleA=0,angleB=-90"))

def makePlot(x,y,prefix,type):
    plot.gcf().set_size_inches(x,y)
    #plot.tight_layout()
    plot.savefig('img/' + prefix + '-' + type + '-' +
                 str(x) + 'x' + str(y) + '.png', dpi=200)
