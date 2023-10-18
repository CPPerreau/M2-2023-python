#!/usr/bin/python3
# -*-coding:UTF-8 -*
'''
Created on 12 october 2020
@author: Christine PLUMEJEAUD-PERREAU, U.M.R 7266 LIENSs
Master 2 course : Web programming with python

Introduce Bokeh
1. Make your first Hello World using Flask templating 
2. Build a viz using dummy figures to show a graphic in the Web page using Bokeh
'''
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/vizports')
def bokeh():
    
    from bokeh.io import show
    from bokeh.models import ColumnDataSource
    import bokeh.palettes as bp
    from bokeh.plotting import figure
    from bokeh.transform import factor_cmap
    import pandas as pd
    import requests
    import folium
    from folium.plugins import MarkerCluster 
    from IPython.display import display
    
    url_to_read = "http://data.portic.fr/api/ports?param=&shortenfields=false&both_to=false&date=1787"

    resp = requests.get(url_to_read) #Récuperer les données
    df = pd.DataFrame(resp.json())
    
    test = df.groupby('admiralty')['ogc_fid'].count()
    fruits = [i for i in test.index]
    counts = [i for i in test.values]
    
    #fruits = df.groupby('admiralty').count()['admiralty']
    #counts = df.groupby('admiralty')['ogc_fid'].count()
    
    source = ColumnDataSource(data=dict(titi=fruits, toto=counts))
    
    p = figure(x_range=fruits, height=700,width=1200, title="Count of ports by admiralties")
    p.xaxis.major_label_orientation = "vertical" #Math.pi/2
    p.vbar(x='titi', top='toto', width=0.9, source=source,
           line_color='white', fill_color=factor_cmap('titi', palette=bp.turbo(len(fruits)), factors=fruits))
    
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.y_range.end = 9
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"
    
    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(p)
    html = render_template(
        'modif_template.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return html

if __name__ == '__main__':
    app.run(debug=True, port=5050)