#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 22:02:43 2020

@author: root
"""

import json
import plotly

with open('BJJHeroesStats.json', 'r') as fp:
    stats = json.load(fp)

"""here's a function that will create a plotly-compatible trace 
from our final list of stats and the stats we want as our x and y"""
def makePlot(data, x_stat, y_stat, list_of_minimums): 
    #list of minimums is a list of tuples where (stat to be limited, limit as an integer)
    data = data
    for minimum in list_of_minimums:
        data = statMinimum(data, minimum[0], minimum[1])
    
    x = []
    y = []
    text = list(data.keys())
    for fighter in data.keys():
        x.append(data[fighter][x_stat])
        y.append(data[fighter][y_stat])
    trace = {'x':x, 
              'y':y,
              'mode': 'markers',
              'text': text}
    return trace

def statMinimum(data, stat, minimum):
    new_data = {}
    for fighter in list(data.keys()):
        if data[fighter][stat] >= minimum:
            new_data[fighter] = data[fighter]
    return new_data


parameters = [("total_matches", 0)]

fighter_trace = makePlot(stats, 'sub_variety', 'win_percent', parameters)

plotly.offline.plot([fighter_trace])

