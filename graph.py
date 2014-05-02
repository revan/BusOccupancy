#!/bin/python3
import click
import json
import pandas as pd
from filter import filter
from grid import plotGrid
from unique import plotUnique
from packets import plotPackets
from packethist import plotPacketHistogram
from segments import plotSegments

@click.command()
@click.argument('infile', type=click.File(), default='data/in.json')
@click.option('-t', '--graph-type', help='Type of graph to create',
              required=True,
              type=click.Choice(["unique","packets","grid","packethist", "segments"]))
@click.option('-r', '--router-filtering', type=click.BOOL, default=True,
              help="Filter routers out of packet list.")
@click.option('-s', '--strength-filtering', type=click.INT, default=0,
              help="Filter packets with strength less than the given value.")
@click.option('-b', '--blank-strength-filtering', type=click.BOOL,
              help="Filter packets with no strength field.")
@click.option('-e', '--end-time', type=click.INT, default=0,
              help="Specify an end time for the dataset.")
@click.option('-c', '--coincidence', type=click.INT, default=0,
              help="Specify under what coincidence data should be rendered.")
@click.option('-s', '--binsize', type=click.INT, default=3,
              help="Specify a binsize for graphs which use bins.")
@click.option('-l', '--label-file', type=click.File())
def graph(infile, graph_type, router_filtering, strength_filtering,
          blank_strength_filtering, end_time, coincidence, binsize, label_file):

    jason = json.load(infile)
    infile.close()
    jason["packets"] = pd.DataFrame(jason["packets"])

    filter(jason, rmRouters=router_filtering, strength=strength_filtering,
           removeBlankStr=blank_strength_filtering)

    if(graph_type == "unique"):
        plotUnique(jason, binsize=binsize, labels=None, endTime=end_time)
    elif(graph_type == "packets"):
        plotPackets(jason, binsize=binsize, labels=None, endTime=end_time)
    elif(graph_type == "grid"):
        plotGrid(jason, coincidence=coincidence, labels=None, endTime=end_time)
    elif(graph_type == "packethist"):
        plotPacketHistogram(jason, coincidence=coincidence, labels=None)
    elif(graph_type == "segments"):
        plotSegments(jason, labels=None)

if __name__ == '__main__':
    graph()
