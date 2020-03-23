#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 21:15:46 2020

@author: root
"""

import plotly
import json

#plotly.offline.init_notebook_mode(connected=True)
# we repeat these first lines just to keep the code together  

with open('BJJHeroesRecordsScrapeDirectLong.json', 'r') as fp:
    percentages = json.load(fp)
with open('BJJHeroesRecordsScrape.json', 'r') as fp:
    records = json.load(fp)

def fighterExperienceMinimum(list_of_fighters, minimum_matches):
    final_list =[]
    for fighter in list_of_fighters:
        if len(fighter['matches']) >= minimum_matches:
            final_list.append(fighter['name'])
    return final_list

def dataFilter(list_of_fighters, filter_list):
    final_list =[]
    for fighter in list_of_fighters:
        if filter_list.__contains__(fighter['name']):
            final_list.append(fighter)
    return final_list


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

final_data = dataFilter(percentages, fighterExperienceMinimum(records, 120))

# All that, and it doesn't even look good :(
plotly.offline.plot([makePlot(final_data)])