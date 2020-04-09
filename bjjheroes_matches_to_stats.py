#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:48:54 2020

@author: root
"""

import json
import re

with open('bjjheroes_matches.json', 'r') as fp:
    records = json.load(fp)
    
def winCount(fighter):
    return len(list(filter(lambda fight: (fight['outcome'] == 'W'), fighter['matches'])))

def byPoints(method):
    digit = re.compile(r'\d')
    non_sub_methods = ["Points",
                       'Adv',
                       'DQ',
                       'Referee Decision',
                       'N/A']
    if method in non_sub_methods or digit.search(method) != None:
        return True
    else:
        return False

def subCount(fighter):
    return len(list(filter(lambda fight: (fight['outcome'] == 'W') & (not byPoints(fight['method'])), fighter['matches'])))

def matchCount(fighter):
    return len(fighter['matches'])

def winPercent(fighter):
    return winCount(fighter)/matchCount(fighter) * 100

def subPercent(fighter):
    if winCount(fighter) > 0:
        return subCount(fighter)/winCount(fighter) * 100
    else:
        return 0

def legLockCount(fighter): 
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

def legLockPercent(fighter):
    if subCount(fighter) > 0:
        return legLockCount(fighter)/subCount(fighter) * 100
    else:
        return 0

def subVariety(fighter):
    fight_list = list(filter(lambda fight: (fight['outcome'] == 'W') & (not byPoints(fight['method'])), fighter['matches']))
    submission_list = list(map(lambda fight: fight['method'], fight_list))
    return len(list(set(submission_list)))

def yearsActive(fighter):
    years = list(map(lambda fight: fight['year'], fighter['matches']))
    years = list(set(years))
    years.sort()
    return years

def matchesByYear(fighter, year):
    fighter_record = list(filter(lambda match: match['year'] == year, fighter['matches']))
    return {'name': int(year), 'matches': fighter_record}

def yearsActiveCount(fighter):
    return len(yearsActive(fighter))

def weightClasses(fighter):
    weights = list(map(lambda fight: fight['weight'], fighter['matches']))
    return list(set(weights))

"""Here are some functions that will clean and filter the weight class data"""
def removeZeroPad(weight):
    if weight[0] == 'O':
        return weight[1:]
    else:
        return weight

def weightClassesClean(fighter):
    weights = weightClasses(fighter)
    clean_weights = []
    for weight in weights:
        clean_weights.append(removeZeroPad(weight))
    return list(set(clean_weights))

def isWeightClass(name):
    classes = ['89KG', '80KG', '99+KG', '65KG', 
               '75KG', '61KG', '76KG', '100KG', 
               '60KG', '74KG', '62 KG', '124KG', 
               '90KG', '88kg', '95KG', 'R1', 
               'LWABS', '97KG', '87KG', '91KG', 
               '55KG', 'U110KG', '109KG', 'U77KG', 
               'N/A', '60+KG', '70kg', 'HWABS', 
               '67KG', '85KG', '100', '57KG', '83KG', 
               '56KG', '100KG+', '3RD', '94KG', 'NA', 
               '72KG', '120KG', '88K', '73KG', '70Kg', 
               '82KF', '77KG', '104KG', '86KG', '66KG', 
               '88KG', '125KG', '69KG', '63KG', '81KG', 
               'ABS', '68KG', '108KG', '105KG', 'F', 
               '98KG', '84KG', '79KG', '93KG', '62KG', 
               '99KG', '110KG', '70KG', '58KG', '92', 
               'SPF', '92KG', '82KG', 'SF', '64KG', '78KG']

    if name in classes:
        return True
    else:
        return False
    
def matchesByWeight(fighter, weight):
    fighter_record = list(filter(lambda match: (match['weight'] == weight) or (match['weight'] == 'O' + weight), fighter['matches']))
    return {'name': weight, 'matches': fighter_record}

def createStats(fighter):
    stats = {'sub_percent': subPercent(fighter),
                'win_percent': winPercent(fighter),
                'match_count': matchCount(fighter),
                'win_count': winCount(fighter),
                'leg_lock_count': legLockCount(fighter),
                'sub_variety': subVariety(fighter),
                'sub_count': subCount(fighter),
                'leg_lock_percent': legLockPercent(fighter),
                'years_active': yearsActive(fighter),
                'years_active_count': yearsActiveCount(fighter),
                'weight_classes': weightClassesClean(fighter)}
    if (type(fighter['name']) == int) or (isWeightClass(fighter['name'])):
        return stats
    else:
        stats_by_year = []
        for year in yearsActive(fighter):
            stats_by_year.append((year, createStats(matchesByYear(fighter, year))))
        stats['by_year'] = dict(stats_by_year)
        
        stats_by_weight = []
        for weight in weightClassesClean(fighter):
            stats_by_weight.append((weight, createStats(matchesByWeight(fighter, weight))))
        stats['by_weight'] = dict(stats_by_weight)
        return stats

def convertMatchesToStats(fighter_records):
    return dict(list(map(lambda fighter: (fighter['name'], createStats(fighter)), fighter_records)))

calculated_stats = convertMatchesToStats(records)
print(len(calculated_stats))

with open('bjjheroes_stats.json', 'w') as fp:
    json.dump(calculated_stats, fp, indent=4)
    