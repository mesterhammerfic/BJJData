#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 20:13:49 2020

@author: root
"""

from bs4 import BeautifulSoup
import requests
import json

def getLinks(link):
    """
    Opens the 'link', 
    finds the rows of a table (from a given column), 
    adds the data from each row to a list, 
    returns list of links
    """
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')
    rows = soup.find_all(class_ = 'column-1') #select which column 
    list_of_links = []
    
    for row in rows[1:]: #rows[1:] is used in case first row is a title row (ie there is no useful data here)
        name = row.find('a')
        link = name.attrs['href'] #the data I'm trying to extract
        list_of_links.append(link)
    return list_of_links

def getWinPercent(wins, losses):
    return wins/(wins+losses)*100

def getRecord(link):
    """
    Opens the 'link' and returns a dictionary that contains the name and a list of matches
    matches are dictionaries that contain the outcome of a single match and the method of the outcome
    record = {name: sample name, matches: [{outcome:w, method:RNC}, {outcome:l, method:pts}]}
    """
    source = requests.get('https://www.bjjheroes.com' + link).text
    soup = BeautifulSoup(source, 'lxml')
    fighterID = link[4:]
    table = soup.find('table') #returns None if there is no record available
    
    if table == None or soup.find('span', {'id':"by_sUb_"+fighterID}) == None: #checks if there is a record
        if soup.find('h1') != None:
            name = soup.find('h1').get_text()
            print(name + ' not added')
        return
    else:
        name = soup.find('h1').get_text()
        subs = soup.find('span', {'id':"by_sUb_"+fighterID}).get_text()
        wins = soup.find_all('span', {'class':"t_wins"})[0].get_text()[:-5] #gets wins
        losses = soup.find_all('span', {'class':"t_wins"})[1].get_text()[:-7] #gets losses
        win_percent = getWinPercent(int(wins), int(losses))
        record = {'name':name, 'subs':int(subs),'wins':win_percent} 
        return record

def listAllRecords():
    record_list = []
    links = getLinks('https://www.bjjheroes.com/a-z-bjj-fighters-list')
    count = 0
    total =len(getLinks('https://www.bjjheroes.com/a-z-bjj-fighters-list'))
    for link in links:
        count = count +1
        print(count/total*100)
        record = getRecord(link)
        if record != None:
            record_list.append(record)
    return record_list

records_list = listAllRecords()

with open('BJJHeroesRecordsScrapeDirectLong.json', 'w') as fp:
    json.dump(records_list, fp, indent=4)