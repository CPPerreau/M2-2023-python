#!/usr/bin/python3
# -*-coding:UTF-8 -*
'''
Created on 12 october 2020, Update on 05/11/2023
@author: Christine PLUMEJEAUD-PERREAU, U.M.R 7266 LIENSs
Master 2 course : Web programming with python

Introduce Bokeh
1. Make your first Hello World using Flask templating 
2. Build a viz using dummy figures to show a graphic in the Web page using Bokeh
'''
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from flask import Flask, render_template, request
app = Flask(__name__)
import requests
import pandas as pd

from bokeh.models import ColumnDataSource
import bokeh.palettes as bp
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

import math

def lireData():
    """ Renvoie un dataframe à partir des données lues de l'API"""
    
    url_to_read = "http://data.portic.fr/api/ports?"

    resp = requests.get(url_to_read) #Récuperer les données
    df = pd.DataFrame(resp.json())
    return df
    
@app.route('/formAmiraute')
def lire_param():
    """ Prouve que le serveur recoit bien le formulaire avec le paramètre admiralty"""
    param = request.args.get("admiralty")
    if (param != None and param == 'Marseille') :
        print(param)
    else : 
        print("une autre amirauté")
    
    #Appeler la redéfinition du graphique avec ce paramètre
    return build_viz_with_param(param)

@app.route('/formviz3')
def build_viz_with_param(msg = 'ma premiere visite'):
    """ Compute the figure to send it into the template
        msg default value is 'ma premiere visite'
        Then, msg will take the value of the param of /formAmiraute
    """

    df = lireData()
    
    test = df.groupby('admiralty')['ogc_fid'].count()
    fruits = [i for i in test.index]
    counts = [i for i in test.values]
    
    #fruits = df.groupby('admiralty').count()['admiralty']
    #counts = df.groupby('admiralty')['ogc_fid'].count()
    
    source = ColumnDataSource(data=dict(titi=fruits, toto=counts))
    
    p = figure(x_range=fruits, height=700,width=1200, title="Count of ports by admiralties")
    p.xaxis.major_label_orientation = math.pi/2
    p.vbar(x='titi', 
           top='toto', 
           width=0.9, 
           source=source,
           line_color='white', 
           fill_color=factor_cmap('titi', palette=bp.turbo(len(fruits)), factors=fruits))
    
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.y_range.end = max(counts)*1.2
    #p.legend.orientation = "horizontal"
    #p.legend.location = "top_center"
    
    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(p)
    html = render_template(
        'forms_amiraute.html',
        plot_script=script,
        plot_div=div,
        message=msg,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return html

if __name__ == '__main__':
    app.run(debug=True, port=5050)