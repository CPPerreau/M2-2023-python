#!/usr/bin/python3
# -*-coding:UTF-8 -*
'''
Created on 12 october 2020
@author: Christine PLUMEJEAUD-PERREAU, U.M.R 7266 LIENSs
Master 2 course : Web programming with python
Update on 05/11/2023

TP for using HTML forms to build figures with user choices
Used to read and parse data coming from the data.portic.fr API
Then it builds a viz using BOKEH and sends the figure in the template HTML
The figure is changing according to user choices (name of the state)
using Ajax

'''
from flask import Flask, render_template, request, jsonify

import http.client
from io import StringIO, BytesIO, TextIOWrapper
import json
import pandas as pd

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.palettes import Viridis
from bokeh.transform import factor_cmap
import requests
import math
import bokeh.palettes as bp

app = Flask(__name__)
#a global data, we get only once
#df = self.getPorticData(local = False)



def getPorticData(local = False) :
    '''
    you grab data from another Web server
    https://docs.python.org/3.7/library/http.client.html#httpresponse-objects
    #target_url = "http://data.portic.fr/api/ports/?"
    return a dataframe
    '''
    if not local:
        url_to_read = "http://data.portic.fr/api/ports?"
        resp = requests.get(url_to_read) #Récuperer les données      
        data = resp.json()
    else : 
        ## If you read data in a file on your server
        url_to_read = "https://gitlab.huma-num.fr/portic/gazetteer/-/raw/master/maps/ports_1789_4326.json?ref_type=heads&inline=false"
        with open('ports.json', encoding="utf-8") as f:
            data = json.load(f)

    ## Create a dataframe out of json
    df = pd.DataFrame(data)
    
    # Dealing with null values
    df.admiralty.isnull().values.any() #True 
    '''
    values = {'admiralty': 'X'} #, 'state_1789_fr': 'X'
    df = df.fillna(value=values)
    df.admiralty.isnull().values.any() #False 
    '''       
    return df

def build_fig3(df):
    '''
    Bar chart : Pour toutes les amirautés, nombre de ports différents, en couleur différente par nom d'amirauté
    '''
    test = df.groupby('admiralty')['ogc_fid'].count()
    fruits = [i for i in test.index]
    counts = [i for i in test.values]
    
    #fruits = df.groupby('admiralty').count()['admiralty']
    #counts = df.groupby('admiralty')['ogc_fid'].count()
    
    source = ColumnDataSource(data=dict(titi=fruits, toto=counts))
    
    # init a  bar chart:
    # https://docs.bokeh.org/en/latest/docs/user_guide/basic/bars.html 
    
    p = figure(x_range=fruits, height=700,width=1200, title="Number of ports per admiralties in 1787")
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
    return p

def build_fig4(filterAdmiralty):
    '''
    Bar chart : nombre de citations (volume du traffic entrant ou sortant) de chaque port contenus dans l'amirauté sélectionnée
    '''
    df = getPorticData(local = False)
    
    ## filter the dataset to keep only ports of the given admiralty
    if (filterAdmiralty=='Unknown') :
        df = df[df.admiralty.isnull() ]
    else :
        df = df[df.admiralty.eq(filterAdmiralty) ]
    print(df.shape)
            
    source = ColumnDataSource(data=dict(names=df['toponyme_standard_fr'], counts=df['total']))

    # init a  bar chart:
    # https://docs.bokeh.org/en/latest/docs/user_guide/basic/bars.html 
    mytitle = "Counts of toponyms citation for ports of %s in 1787"% filterAdmiralty
    p = figure(x_range=df['toponyme_standard_fr'], width=800, height=600, title=mytitle)

    p.vbar(x='names', 
        top='counts', 
        width=0.9, 
        source=source,
       line_color='white', 
       fill_color='navy')
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.y_range.end = max(df['total'])*1.2
    p.xaxis.major_label_orientation = math.pi/2
    
    return p

def build_viz_withparam(df, filterAdmiralty=None):
    #print(filterAdmiralty)
    if (filterAdmiralty is not None) :
        return build_fig4(filterAdmiralty)
    else :
        return build_fig3(df)


@app.route('/')
def index():
    """
    Initial plot 
    """
    
    df = getPorticData(local = False)
    df = df[df.admiralty.notnull()  ] 
    list_toselect = (df.admiralty).unique()
    
    liste_options = list()
    option_str = '<option value="%s">%s</option>'
    #<option value="Toulon">Toulon</option>
    for items in list_toselect:
        test = option_str %(items, items)
        #print(test)
        liste_options.append(test)
    
    fig = build_viz_withparam(df)

    # grab the static resources
    js_resources = INLINE.render_js()
    #print(js_resources)
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)
    


    html = render_template(
        'ajax.html',
        plot_script=script,
        plot_div=div,
        liste_options = ' '.join(liste_options),
        js_resources=js_resources,
        css_resources=css_resources,
    )

    return html



@app.route('/ajaxviz', methods=['GET','POST'])
def viz_ajax():
    df = getPorticData(local = False)

    #Parse the param
    param = request.args.get("admiralty")
    
    #Appeler la redéfinition du graphique avec ce paramètre
    fig = build_viz_withparam(df, param)
    
    # render template
    script, div = components(fig)

    # pass the div and script to render_template    
    return jsonify(
        html_plot=render_template('update_figure.html', plot_script=script, plot_div=div)
    )



if __name__ == '__main__':
    app.run(debug=True, port=5050)

