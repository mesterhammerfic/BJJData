#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 21:15:46 2020

@author: root
"""

import plotly
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

"""We also need a function that will remove fighters from a list if 
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




"""we set our minimum number of fights, filter our fighter data and create our
fighter trace"""
num_of_fights = 0
filter_list = fighterExperienceMinimum(records, num_of_fights)
final_data = dataFilter(percentages, filter_list)
fighter_trace = makePlot(final_data)


plotly.offline.plot([fighter_trace])