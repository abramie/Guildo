#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 10 10:00:55 2022

@author: jrouss
"""
import urllib3
import html5lib
import xml.etree.ElementTree as ET


""" Gestion import web"""




url = 'https://forum.laguilde-poitiers.com/viewforum.php?f=10'
#url='https://www.google.com'
#url='https://urllib3.readthedocs.io/en/stable/reference/urllib3.connection.html'

http = urllib3.PoolManager()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
print("before request")
r = http.request('GET',url, headers=headers )
print("after")
#r= urllib3.request.urlopen(url)
r.status
r.data
#document = html5lib.parse(r.data)
#print (r.data)
document = html5lib.parse(r.data,namespaceHTMLElements=False)

for div in document.iter('div'):
    if div.attrib.get("class") == "forumbg":
        print("found")
    else:
        print(div.attrib.get("class"))
        
print("end")