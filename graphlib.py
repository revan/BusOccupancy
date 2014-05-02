import matplotlib.pyplot as plot
import json

def annotate(label, x, y, xoff=0, yoff=0):
    plot.annotate(label, xy=(x, y), xytext=(xoff, yoff),
                  textcoords="offset points",
                  bbox=dict(boxstyle="round", fc="#d3d3d3", ec="#a8a8a8"),
                  arrowprops=dict(arrowstyle="fancy", fc="#d3d3d3",
                                  ec="#a8a8a8", connectionstyle=
                                  "angle3,angleA=0,angleB=-90"))

def wideAnnotate(plot, hist, binsize, file='data/sched.json'):
    phil = open(file)
    jason = json.load(phil)
    for stop in jason:
        x = stop["start"]
        y = hist[int(x)/3]
        annotate(stop["name"], x, y, 50, 60)


def squareAnnotate(plot, file='data/sched.json', ymax=0):
    phil = open(file)
    jason = json.load(phil)
    for stop in jason:
        x = stop["start"]
        plot.plot([0,x],[x,x],'purple',linewidth=1)
        plot.plot([x,x],[x,ymax],'purple',linewidth=1)
        annotate(stop["name"], x, x, 10, -10)

def makePlot(x,y,prefix,type):
    plot.gcf().set_size_inches(x,y)
    #plot.tight_layout()
    plot.savefig('img/' + prefix + '-' + type + '-' +
                 str(x) + 'x' + str(y) + '.png', dpi=200)

def makeWidePlot(prefix,type):
    plot.gcf().set_size_inches(16,7)
    plot.savefig('img/' + prefix + '-' + type +
                 '-wide.png', dpi=200)

def makeSquarePlot(prefix,type):
    plot.gcf().set_size_inches(8,7.5)
    plot.savefig('img/' + prefix + '-' + type +
                 '-square.png', dpi=200)
