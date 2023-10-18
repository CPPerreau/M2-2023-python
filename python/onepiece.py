# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 20:54:59 2022

@author: cplume01
"""
from PIL import Image
import requests

chapter = '1'
i=2
j=f'0{i}'

pic_url = f'https://www.scan-vf.net/uploads/manga/one_piece/chapters/chapitre-{chapter}/{j}.webp'

print(pic_url)
headers = {'user-agent': 'my-agent/1.0.1'}
response = requests.get(pic_url, stream=True, headers=headers)
if not response.ok:
    #stop
    print("no more image for this chapter")
else:
    #save the data
    print("saving into "+f'resultats/chapitre-{chapter}_{j}.webp')
    filename = f'resultats/chapitre-{chapter}_{j}.webp'

    output = open(filename, "wb")
    for block in response.iter_content(1024):
        if not block:
            break
        output.write(block)
    output.close()
    
    #convert into the image
    print("convert into "+f'resultats/chapitre-{chapter}_{j}.png')
    im = Image.open(f'resultats/chapitre-{chapter}_{j}.webp').convert('RGB')
    im.save(f'resultats/chapitre-{chapter}_{j}.png', 'png')

