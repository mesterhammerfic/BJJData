#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 12:53:21 2020

@author: root
"""

import json
import re

"""first we open the data files"""
with open('BJJHeroesRecordsScrapeDirectLong.json', 'r') as fp:
    percentages = json.load(fp)
with open('BJJHeroesRecordsScrape.json', 'r') as fp:
    records = json.load(fp)
    
    
"""now we need to find the percentage of how many leglocks out of their 
total wins for each fighter"""
def countLegLocks(fighter): 
    #takes a fighter [{name = 'name'}, {matches = [{....}]}] and tallies the leglock wins
    leglock_names = ['HEEL HOOK', 
                     'KNEEBAR', 
                     'TOE HOLD', 
                     'INSIDE HEEL HOOK', 
                     'OUTSIDE HEEL HOOK', 
                     'CALF SLICER',
                     'STRAIGHT ANKLE LOCK',
                     'FOOTLOCK']
    return len(list(filter(lambda fight: (fight['outcome'] == 'W') & (fight['method'].upper() in leglock_names), fighter['matches'])))


def countWins(fighter):
    return len(list(filter(lambda fight: (fight['outcome'] == 'W'), fighter['matches'])))

"""we also need a cleaner way to store data."""
def combineStats(percent, record):
    new_fighter_dict = {}
    for fighter in percent:
        new_fighter_dict[fighter['name']] = {
                'sub_percent': fighter['subs'],
                'win_percent': fighter['wins']
                }
    for fighter in record:
        if fighter['name'] in new_fighter_dict.keys():
            new_fighter_dict[fighter['name']]['total_matches'] = len(fighter['matches'])
            new_fighter_dict[fighter['name']]['win_count'] = countWins(fighter)
            new_fighter_dict[fighter['name']]['leg_lock_count'] = countLegLocks(fighter)
            new_fighter_dict[fighter['name']]['sub_variety'] = submissionVariety(fighter)
    return new_fighter_dict

"""now calculating the percentage will be easy"""
def calculateLegLockPercent(stat_list_original):
    stat_list = stat_list_original
    for fighter in stat_list.keys():
        stat_list[fighter]['sub_count'] = round((stat_list[fighter]['sub_percent']/100) * stat_list[fighter]['win_count'])
    for fighter in stat_list.keys():
        if stat_list[fighter]['sub_count'] != 0:
            stat_list[fighter]['leg_lock_percent'] = stat_list[fighter]['leg_lock_count'] / stat_list[fighter]['sub_count'] *100
        else:
            stat_list[fighter]['leg_lock_percent'] = 0
    return stat_list

"""I want to find the set of all distinct submissions that a given fighter
has won with."""
def byPoints(method):
    digit = re.compile(r'\d')
    if method == "Points" or method == 'Adv' or method =='DQ' or method == 'Referee Decision':
        return True
    elif digit.search(method) != None:
        return True
    else:
        return False

def submissionVariety(fighter):
    fight_list = list(filter(lambda fight: (fight['outcome'] == 'W') & (not byPoints(fight['method'])), fighter['matches']))
    submission_list = list(map(lambda fight: fight['method'], fight_list))
    return len(list(set(submission_list)))
    
stats = combineStats(percentages, records)
stats_new = calculateLegLockPercent(stats)

with open('BJJHeroesStats.json', 'w') as fp:
    json.dump(stats_new, fp, indent=4)