# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 18:17:08 2022

@author: cplume01
"""
#import http.client
#from io import StringIO, BytesIO, TextIOWrapper
import json
import pandas as pd


import requests



##Ancienne méthode
"""
print("Ancienne méthode")
conn = http.client.HTTPConnection("data.portic.fr")
conn.request("GET", "/api/ports/?shortenfields=false&both_to=false&date=1787")
r1 = conn.getresponse()
print(r1.status, r1.reason)
print(r1)

data1 = r1.read()  # This will return entire content.
type(data1) #bytes
b = BytesIO(data1)
b.seek(0) #Start of stream (the default).  pos should be  = 0;
data = json.load(b)
type(data)
"""

## Nouvelle méthode
## https://requests.readthedocs.io/en/latest/
print("Nouvelle méthode")
url = "http://data.portic.fr/api/ports/?shortenfields=false&both_to=false&date=1787"
r = requests.get(url)
#print(r.text)
print(type(r.json()))

data = r.json()

 #<class 'list'>
df = pd.DataFrame(data)

print(df.shape) #(1426, 25)

print(df.admiralty.unique())

# Dealing with null values
df.admiralty.isnull().values.any() #True 
values = {'admiralty': 'X'}
df = df.fillna(value=values)
df.admiralty.isnull().values.any() #False 

# Listing of admiralties
df.admiralty.unique() # array(['X'], dtype=object)
df.admiralty.unique().size #52

print(df)
# How many ports by admiralty ?
df.groupby('admiralty')['ogc_fid'].count()

# How many ports by state_1789_fr ?
df.groupby('state_1789_fr')['ogc_fid'].count()


