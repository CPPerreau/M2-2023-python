# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 17:22:04 2022
Show how to read data coming from a server : comparaison de urlopen et requests
Show how to save them into a local file. 
@author: cplume01
"""

#import cProfile
import json
import pprint

from urllib.request import urlopen
import requests

def custom_pretty_print():
    url_to_read = "https://www.cbcmusic.ca/Component/Playlog/GetPlaylog?stationId=96&date=2018-11-05"
    with urlopen(url_to_read) as resp:
        pretty_json = json.dumps(json.load(resp), indent=2)
    print(f'Pretty: {pretty_json}')


def custom_pretty_print2(url_to_read):
    with urlopen(url_to_read) as resp:
        pretty_json = json.dumps(json.load(resp), indent=2)
    print(f'Pretty: {pretty_json}')



def pprint_json():
    url_to_read = "https://www.cbcmusic.ca/Component/Playlog/GetPlaylog?stationId=96&date=2018-11-05"
    with urlopen(url_to_read) as resp:
        info = json.load(resp)
    pprint.pprint(info)
    
    
def pprint_json2(url_to_read):
    with urlopen(url_to_read) as resp:
        info = json.load(resp)
    pprint.pprint(info)
    
    
if __name__ == '__main__':
    print("with pprint_json")
    url = "https://www.cbcmusic.ca/Component/Playlog/GetPlaylog?stationId=96&date=2018-11-05"
    pprint_json2(url)
    
    url_to_read = "http://data.portic.fr/api/ports/?param=uhgs_id,geom,toponyme_standard_fr,state_1789_fr&shortenfields=false&both_to=false&date=1787&format=geojson"
# =============================================================================
#     print("with custom_pretty_print2")
#     custom_pretty_print2(url_to_read)
# =============================================================================
    
# =============================================================================
#     print("with pprint_json2")
#     pprint_json2(url_to_read)
# =============================================================================
    

    filename = "resultats/export3_port_geojson.geojson"

    print("output in a file :"+filename)
    #1.
    output = open(filename, "w")
    
    resp = requests.get(url_to_read)
    pretty_json = json.dumps(resp.json(), indent=2) 
    
    #2.
    output.write(pretty_json)   
    #3.
    output.close()
        