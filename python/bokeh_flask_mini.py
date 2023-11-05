#!/usr/bin/python3
# -*-coding:UTF-8 -*
'''
Created on 12 october 2020
Updated on 31/10/2023
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

@app.route('/bokeh')
def bokeh():
    # init a basic bar chart:
    # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
    fig = figure(width=600, height=600)
    fig.vbar(
        x=[1, 2, 3, 4],
        width=0.5,
        bottom=0,
        top=[1.7, 2.2, 4.6, 3.9],
        color='navy'
    )

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

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