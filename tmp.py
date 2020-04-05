#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 21:15:46 2020

@author: root
"""

import json

"""first we open the data files"""
with open('BJJHeroesRecordsScrapeDirectLong.json', 'r') as fp:
    percentages = json.load(fp)
with open('BJJHeroesRecordsScrape.json', 'r') as fp:
    records = json.load(fp)

"""now we need a function that will give a list of fighters who 
have at least a certain number of matches"""
def fighterExperienceMinimum(list_of_fighters, minimum_matches):
    final_list =[]
    for fighter in list_of_fighters:
        if len(fighter['matches']) >= minimum_matches:
            final_list.append(fighter['name'])
    return final_list

"""We also need a function that will fighters from a list if 
their name appears on another list (we call the filter list)"""
def dataFilter(list_of_fighters, filter_list):
    final_list =[]
    for fighter in list_of_fighters:
        if filter_list.__contains__(fighter['name']):
            final_list.append(fighter)
    return final_list

"""here's a function that will create a plotly-compatible trace 
from our final list of fighter data"""
def makePlot(data):
    wins_list = []
    subs_list = []
    names_list = []
    for fighter in data:
        wins_list.append(fighter['wins'])
        subs_list.append(fighter['subs'])
        names_list.append(fighter['name'])
    trace = {'x':wins_list, 
              'y':subs_list,
              'mode': 'markers',
              'text': names_list}
    return trace




"""this is a function that creates a plotly-compatible trace for a line
with any given slope and y-intercept. This will be used to find a 
starting point for our visualization"""
def makeLine(m, b, start_x, end_x, step_size):
    lineTrace = {'x':[], 'y':[], 'mode':'lines'}
    for x in range(start_x, end_x, step_size):
        lineTrace['y'].append(m*x+b)
        lineTrace['x'].append(x)
    return lineTrace




"""Now I will make a function that will take a plotly-compatible trace and run 
the RSS algorithm"""
"""make a function the creates (x, y) tuples out of a plotly_trace dictionary"""
def makeXYTuples(plotly_trace):
    list_of_tuples = []
    for index in range(0, len(plotly_trace['x'])):
        list_of_tuples.append((plotly_trace['x'][index], plotly_trace['y'][index]))
    return list_of_tuples
"""And here's an individual RSS calculator so we can easily map this for 
a whole list"""
def indRSS(m,b,known_x, known_y):
    return (known_y - (m*known_x-b))**2

def RSS(m,b, plotly_trace):
    list_of_dif = []
    list_of_tuples = makeXYTuples(plotly_trace)
    for xy in list_of_tuples: #each xy is a (x, y), thus xy[0] returns the x coordinate
        list_of_dif.append(indRSS(m, b, xy[0], xy[1]))
    return sum(list_of_dif)
"""we set our line values and create the line trace"""
m = 26/23
b = 40
line_trace = makeLine(m, b, 40, 110, 10)

"""we set our minimum number of fights, filter our fighter data and create our
fighter trace"""
num_of_fights = 0
filter_list = fighterExperienceMinimum(records, num_of_fights)
final_data = dataFilter(percentages, filter_list)
fighter_trace = makePlot(final_data)

for fighter in fighter_trace['y']:
    print(fighter)