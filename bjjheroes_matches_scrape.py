#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 14:46:26 2019

@author: root
"""

import requests
from bs4 import BeautifulSoup
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

def getRecord(link):
    """
    Opens the 'link' and returns a dictionary that contains the name and a list of matches
    matches are dictionaries that contain the outcome of a single match and the method of the outcome
    record = {name: sample name, matches: [{outcome:w, method:RNC}, {outcome:l, method:pts}]}
    """
    source = requests.get('https://www.bjjheroes.com' + link).text
    soup = BeautifulSoup(source, 'lxml')
    
    table = soup.find('table') #returns None if there is no record available
    
    if table == None:
        if soup.find('h1') != None:
            name = soup.find('h1').get_text()
            print(name + ' not added')
        return
    else:
        name = soup.find('h1').get_text()
        print(name + ' being added')
        record = {'name':name, 'matches': []} 
        all_rows=table.find_all('tr')
        all_matches = all_rows[1:] #removes header from table
        for match in all_matches:
            columns = match.find_all('td') #splits each row (a single match) into the columns
            if len(columns)<7:
                return
            else:
                outcome = columns[2].get_text()
                method = columns[3].get_text()
                year = columns[7].get_text()
                weight = columns[5].get_text()
                record['matches'].append({'outcome':outcome, 'method':method, 'year': year, 'weight':weight})
            print(name+' added')
        return record
            
def listAllRecords():
    record_list = []
    links = getLinks('https://www.bjjheroes.com/a-z-bjj-fighters-list')
    count = 0
    total =len(getLinks('https://www.bjjheroes.com/a-z-bjj-fighters-list'))
    for link in links:
        count = count +1
        print(count/total*100) #this is simply to display the progress of the scrape while you're running it
        record = getRecord(link)
        if record != None:
            record_list.append(record)
        
    return record_list


records_list = listAllRecords()

print(len(records_list))


with open('bjjheroes_matches.json', 'w') as fp:
    json.dump(records_list, fp, sort_keys=True, indent=4)
    
