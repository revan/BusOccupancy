# This library exists so that we have synchronized settings across graphs --
#  our graphs should have the same style and size, so that the report does not
#  appear erratic.
import matplotlib.pyplot as plot
import json


def annotate(label, x, y, xoff=0, yoff=0):
    plot.annotate(label, xy=(x, y), xytext=(xoff, yoff),
                  textcoords="offset points",
                  bbox=dict(boxstyle="square,pad=0.1", fc="#d3d3d3", ec="#a8a8a8"),
                  arrowprops=dict(arrowstyle="->", fc="#d3d3d3",
                                  ec="#a8a8a8", connectionstyle=
                                  "angle3,angleA=0,angleB=-90"))


def wideAnnotate(plot, hist, binsize, ymax=10000, file='data/sched.json'):
    phil = open(file)
    jason = json.load(phil)
    yprev = -ymax
    for stop in reversed(jason):
        x = stop["start"]
        y = hist[int(x)/binsize]
        annotate(stop["code"], x, y, 15, 25 if abs(yprev-y) < ymax/20 else 15)
        yprev = y


def squareAnnotate(plot, file='data/sched.json', ymax=0):
    phil = open(file)
    jason = json.load(phil)
    for stop in jason:
        x = stop["start"]
        plot.plot([0, x], [x, x], 'purple', linewidth=1)
        plot.plot([x, x], [x, ymax], 'purple', linewidth=1)
        annotate(stop["code"], x, x, 10, -10)


def makePlot(x, y, prefix, type):
    plot.gcf().set_size_inches(x, y)
    plot.savefig('img/' + prefix + '-' + type + '-' +
                 str(x) + 'x' + str(y) + '.png', dpi=200)


def makeWidePlot(prefix, type):
    plot.gcf().set_size_inches(3.4, 3.4)
    plot.tight_layout()
    plot.savefig('img/' + prefix + '-' + type + '-wide.png',
                 bbox_inches='tight')
    plot.savefig('img/' + prefix + '-' + type + '-wide.pgf',
                 bbox_inches='tight')


def makeSquarePlot(prefix, type):
    plot.gcf().set_size_inches(3.4, 6.5)
    plot.tight_layout()
    plot.savefig('img/' + prefix + '-' + type + '-square.pgf',
                 bbox_inches='tight')
