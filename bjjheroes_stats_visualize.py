#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 22:02:43 2020

@author: root
"""

import json
import plotly

with open('bjjheroes_stats.json', 'r') as fp:
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
              'text': text,
              'name': 'BJJData'}
    return trace

def makePlotByYear(data, name, y_stat): 
    #list of minimums is a list of tuples where (stat to be limited, limit as an integer)
    data = data[name]['by_year']

    
    x = list(data.keys())
    y = []
    text = list(data.keys())
    for fighter in data.keys():
        y.append(data[fighter][y_stat])
    trace = {'x':x, 
              'y':y,
              'mode': 'lines',
              'text': text,
              'name': name + ' | ' + y_stat
              }
    return trace

def makePlotByWeight(data, name, y_stat): 
    #list of minimums is a list of tuples where (stat to be limited, limit as an integer)
    data = data[name]['by_weight']

    
    x = list(data.keys())
    y = []
    text = list(data.keys())
    for fighter in data.keys():
        y.append(data[fighter][y_stat])
    trace = {'x':x, 
              'y':y,
              'mode': 'markers',
              'text': text,
              'name': name + ' | ' + y_stat
              }
    return trace

def statMinimum(data, stat, minimum):
    new_data = {}
    for fighter in list(data.keys()):
        if data[fighter][stat] >= minimum:
            new_data[fighter] = data[fighter]
    return new_data

"""all fighters visualization"""
#parameters = [("win_percent", 70)]
#
#fighter_trace = makePlot(stats, 'years_active_count', 'sub_percent', parameters)
#
#plotly.offline.plot([fighter_trace])

"""by year"""
fighter_trace0 = makePlotByYear(stats, 'Gordon Ryan', 'win_percent')
fighter_trace1 = makePlotByYear(stats, 'Gordon Ryan', 'leg_lock_percent')
fighter_trace2 = makePlotByYear(stats, 'Gordon Ryan', 'match_count')
fighter_trace3 = makePlotByYear(stats, 'Gordon Ryan', 'sub_percent')

plotly.offline.plot([fighter_trace0, fighter_trace1, fighter_trace2, fighter_trace3])

"""by weight"""
#name = 'Marcelo Garcia'
#fighter_trace0 = makePlotByWeight(stats, name, 'sub_percent')
#fighter_trace1 = makePlotByWeight(stats, name, 'win_percent')
#fighter_trace2 = makePlotByWeight(stats, name, 'match_count')
#plotly.offline.plot([fighter_trace0,fighter_trace1,fighter_trace2])

