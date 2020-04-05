#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:45:56 2020

@author: root
"""

import scrapy
class EventSpider(scrapy.Spider):
    name='Events'
    
    def start_requests(self):
        urls = [
            'https://smoothcomp.com/en/events/past?page=1',
            'https://smoothcomp.com/en/events/past?page=2',
            'https://smoothcomp.com/en/events/past?page=3',
            'https://smoothcomp.com/en/events/past?page=4',
            'https://smoothcomp.com/en/events/past?page=5']
        return [scrapy.Request(url=url, callback=self.parse)
            for url in urls]
    
    def parse(self, response):
        url = response.url
        first_event = response.css('html body div.content div#searchForm.event-finder section.padding-xs-0 div.container.container-events div.event-list div.margin-bottom-xs-64 div.row.event-section div.col-xs-6.col-md-3.col-sm-clear-2.col-xs-clear-2.col-md-clear-4.col-lg-clear-4 div.panel.no-border.event.event-card div.panel-body h3.event-title.margin-bottom-xs-8 a.event-title.color-inherit::text').get()
        print('URL is: {}'.format(url))
        print('Title is: {}'.format(first_event))