#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 02:06:11 2019

@author: imox
"""

import requests
import json

url = 'https://techpacker.com/blog/ghost/api/v2/content/posts/?key=your-key&page='
totalPages = 9+1
pageNo = 0
links = []

for i in range(1,totalPages):
    pageNo = pageNo + 1
    pageUrl = url+str(pageNo)
    content = requests.get(pageUrl)
    posts = json.loads(content.text)['posts']
    
    for post in posts:
        print(post['url'])
        links.append(post['url'])
    
print(links)
   
import pandas as pd

serialNos = list(range(1,len(links)+1))

df = pd.DataFrame.from_dict({'Number':serialNos,'blog url':links})
df.to_excel('test.xlsx', header=True, index=False)