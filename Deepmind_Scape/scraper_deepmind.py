#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 19:19:32 2021

@author: anasputhawala
"""

#%% Imports / initializations
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
from random import randint

titles = []
summaries=[]
dates=[]
types=[]

#%% Function definitions
def get_titles(match):
    l = []
    for content in match:
        title = content.find('a')
        l.append(title.text.strip())
    return l

def get_summaries(match):
    l = []
    for content in match:
        summary = content.find('p', class_ = 'medium')
        l.append(summary.text.strip())
    return l
    
def get_dates(match):
    l = []
    for content in match:
        footer = content.find('div', class_='footer')
        l.append(footer.find('p').text.strip())
    return l
    
def get_type(match):
    l = []
    for content in match:
        header = content.find('div', class_=['header', 'category'])
        l.append(header.find_all('p', class_="caption")[-1].text.strip())
    return l

def flatten(input_list):
    return np.concatenate(input_list).ravel().tolist()
#%% Instantiate driver
driver = webdriver.Chrome('/Users/anasputhawala/Downloads/chromedriver')

pages = np.arange(1,9)
for page in pages:
    driver.get(f'https://deepmind.com/blog?page={page}')
    page_source = driver.execute_script('return document.body.innerHTML;')
    
    #Utilize BeautifulSoup to effectively scrape page
    soup = BeautifulSoup(page_source, 'html.parser')

    res = 'content-card-body'

    match = soup.find_all('div', class_=res)
    
    titles.append(get_titles(match))
    
    summaries.append(get_summaries(match))
    
    dates.append(get_dates(match))
    
    types.append(get_type(match))

    sleep(randint(5,10))

driver.quit()
#%% Flatten lists    
titles = flatten(titles)
summaries = flatten(summaries)
dates = flatten(dates)
types = flatten(types)

#%% Sculpt the dataframe
df = pd.DataFrame(list(zip(titles, summaries, dates, types)), columns = ['Title', 'Summary', 'Date', 'Type of Article'])

file_name = 'Deepmind_Scrape.xlsx'
df.to_excel(file_name)
