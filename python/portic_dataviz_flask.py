#!/usr/bin/python3
# -*-coding:UTF-8 -*
'''
Created on 12 october 2020
Updated on 31/10/2023
@author: Christine PLUMEJEAUD-PERREAU, U.M.R 7266 LIENSs
Master 2 course : Web programming with python

TP for using Bokeh to build figures with dynamic data
Used to read and parse data coming from a file
Then it builds a viz using BOKEH and sends the figure in the template HTML
'''
from flask import Flask, render_template


import json
import pandas as pd

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6, all_palettes,Turbo256, linear_palette
from bokeh.transform import factor_cmap
import requests

app = Flask(__name__)


def getPorticData(local = True) :
    '''
    you read data from a local file or a remote github
    https://docs.python.org/3.7/library/http.client.html#httpresponse-objects
    #target_url = "http://data.portic.fr/api/ports/?shortenfields=false&both_to=false&date=1787"
    '''
    if not local:
        #Set the correct URL
        url_to_read = "http://data.portic.fr/api/ports?"
        resp = requests.get(url_to_read) #Récuperer les données      
        data = resp.json()
    else : 
        ## If you read data in a file on your server (it is a JSON, not a geojson file)
        filename = "C:/Travail/Enseignement/Cours_M2_python/2023/code/resultats/export3_port_geojson.geojson"
        output = open(filename, "r")
        data = json.load(output)
        

    ## Create a dataframe out of json
    df = pd.DataFrame(data)
    
    # Dealing with null values
    df.admiralty.isnull().values.any() #True 
    values = {'admiralty': 'X'}
    df = df.fillna(value=values)
    df.admiralty.isnull().values.any() #False 

    # Listing of admiralties
    df.admiralty.unique() # array(['X'], dtype=object)
    df.admiralty.unique().size #52

    # How many ports by admiralty ?
    df.groupby('admiralty')['ogc_fid'].count()

    # How many ports by belonging_states ?
    values = {'state_1789_fr': 'X'}
    df = df.fillna(value=values)
    df.groupby('state_1789_fr')['ogc_fid'].count()
    #https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html

                        
    ## Check the results
    #df[['toponyme_standard_fr', 'state_1789_fr']]        
    #df.shape

    #print(type(df))
    #df.loc[0, ['toponyme_standard_fr', 'state_1789_fr', 'total']]

    # How many ports cited by belonging_states ?
    
    df2 = df[['state_1789_fr', 'toponyme_standard_fr',  'total']].groupby('state_1789_fr')['total'].sum()
    ## Sort by total     
    df2.sort_values( ascending=False, inplace=True)
    df2 = df2.reset_index() #.add_suffix('_Sum')
    #print(df2.columns)
    #print(df2)
    #print(df2.shape)
    
    
    
    
    return df2

def build_viz(df):
    #print('Nombre états : ' + str(df.shape[0])) #39 
    
    #Filter an outlier (la France)
    print(df.describe())
    print(df.describe().loc['max', 'total'])
    #df = df[df['state_1789_fr'] != 'France']
    df = df[df['total'] != df.describe().loc['max', 'total']]
    
    source = ColumnDataSource(data=dict(names=df['state_1789_fr'], counts=df['total']))

    # init a basic bar chart:
    # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
    # https://docs.bokeh.org/en/latest/docs/user_guide/basic/bars.html#ug-basic-bars
    p = figure(x_range=df['state_1789_fr'], width=800, height=600, title="Counts of toponyms citation for ports per state in 1787")

    '''
    fig = figure(plot_width=600, plot_height=600)
    fig.vbar(
        x=['a', 'b', 'c', 'd', 'e'],
        width=0.5,
        bottom=0,
        top=[1.7, 2.2, 4.6, 3.9, 5],
        color='navy'
    )
    '''

    #https://docs.bokeh.org/en/latest/docs/reference/palettes.html
    #Version 1 : bars are vertical
    p.vbar(x='names', 
           top='counts', 
           width=0.9, 
           source=source, 
           line_color='white', 
           fill_color='navy')
    #factor_cmap('names', palette=linear_palette(Turbo256, df.shape[0]), factors=df['state_1789_fr'])
    #legend_field="names",
    #p.legend.orientation = "vertical"
    #p.legend.location = "top_center"
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.y_range.end = max(df['total'])*1.2

    #Version 2 : bars are horizontal, and we add a tooltip
    #https://docs.bokeh.org/en/latest/docs/user_guide/basic/bars.html#ug-basic-bars
    p = figure(y_range=df['state_1789_fr'], x_range=(0,max(df['total'])*1.2), width=700, height=550, 
           title="Total number of citation for each state for arrival or departures in Portic",
           tooltips="@names  : @counts",
           toolbar_location="below",
           toolbar_sticky=False)  #tools="hover,save", 
    p.hbar(y="names", left=0, right='counts', height=0.4, source=source) #left='Time_min', right='Time_max'

    p.ygrid.grid_line_color = None
    p.xaxis.axis_label = "Occurences of citations (number of departures/arrivals from/in ports)"
    p.outline_line_color = None
    #p.x_range.start = 0
    #p.x_range.end = max(df['total'])*1.2

    #p.xaxis.major_label_orientation = 1.57 # = pi/2 e.g. 90°

    return p

@app.route('/ports')
def show_ports():
    df = getPorticData()
    content = df.to_html()
    return render_template('hello.html', msg=content)

@app.route('/vizports')
def viz_ports():
    df = getPorticData(local = True)

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    fig = build_viz(df)

    # render template
    script, div = components(fig)

    html = render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )

    return html

if __name__ == '__main__':
    app.run(debug=True, port=5050)

