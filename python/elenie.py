import os

from bokeh.models import DatetimeTickFormatter
from bokeh.models import ColumnDataSource, CustomJS, DateSlider, LinearAxis, HoverTool
from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.models.ranges import Range1d
from flask import Flask, render_template, request, jsonify
import pandas as pd
from bokeh.resources import INLINE
from bokeh.embed import components


app = Flask(__name__)

@app.route('/ajaxviz', methods=['GET','POST'])
def change_the_date():
    #Parse the param
    param = request.args.get("chosen_date")
    
    #Here, change the maps
    #Appeler la redéfinition du graphique avec ce paramètre - ici changer les cartes donc ! 
    #fig = build_viz_withparam(df, param)
    
    # render template
    #script, div = components(fig)

    # pass the div and script to render_template  
    '''  
    # if you have more than 1 figure..., push them into the render_template as parameters
    plot1_script=script1, plot1_div=div1
    plot2_script=script2, plot2_div=div2
    # Add also in the HTML template
    {{ plot1_script|indent(4)|safe }}
    {{ plot1_div|indent(4)|safe }}
    {{ plot2_script|indent(4)|safe }}
    {{ plot2_div|indent(4)|safe }}
    #OK ?!
    '''
    
    return jsonify(
        html_plot=render_template('update_message.html', p_msg=param)
    )    
    
@app.route('/')
def bokeh():
    #df = pd.read_excel('Donnees_carte.xlsx', sheet_name='meteo_graphique')
    df=pd.read_csv('C:/Travail/Enseignement/Cours_M2_python/Projet_Elenie/weather.csv', sep=';')
    df = df.rename(columns={"Dates (mois d'aout)": "date", "Vent km/h ": "wind_speed", "Vagues m ": "wave"})
    df['date'] = pd.to_datetime(df['date'])


    source = ColumnDataSource(df)
    original_source = ColumnDataSource(df.copy())
    p = figure(title="Wind Speed and Wave Height Over Time", x_axis_label='Date and Time', y_axis_label='Wind Speed (km/h)',
               x_axis_type='datetime', width=1000, height=400)

    p.xaxis.formatter = DatetimeTickFormatter(
        hours=["%d %B %Y %H:%M"],
        days=["%d %B %Y %H:%M"],
        months=["%d %B %Y %H:%M"],
        years=["%d %B %Y %H:%M"],
    )

    p.line('date', 'wind_speed', source=source, legend_label="Wind Speed (km/h)", color="blue", line_width=2)
    p.extra_y_ranges = {"wave": Range1d(start=df['wave'].min() - 0.1, end=df['wave'].max() + 0.2)}
    p.add_layout(LinearAxis(y_range_name="wave", axis_label="Wave Height (m)"), 'right')
    p.line('date', 'wave', source=source, legend_label="Wave Height (m)", color="red", line_width=2, y_range_name="wave")

    p.legend.location = "top_center"

    hover = HoverTool(tooltips=[
        ("Date", "@date{%F %T}"),
        ("Wind Speed (km/h)", "@wind_speed"),
        ("Wave Height (m)", "@wave")
    ], formatters={'@date': 'datetime'})

    p.add_tools(hover)

    slider = DateSlider(title="Select Date", start=df['date'].min(), end=df['date'].max(), value=df['date'].min(), step=1)

    msg = 'unknown'
    callback = CustomJS(args=dict(original_source=original_source, source=source, slider=slider), code="""
        var data = original_source.data;  // Use the original full dataset
        var f = slider.value;
        console.log(slider.value);
        var date = new Date(f);
        var wind_speed = data['wind_speed'];
        var wave = data['wave'];
        var dates = data['date'];

        var new_wind_speed = [];
        var new_wave = [];
        var new_dates = [];

        for (var i = 0; i < dates.length; i++) {
            if ((new Date(dates[i])).getTime() <= date.getTime()) {
                new_dates.push(dates[i]);
                new_wind_speed.push(wind_speed[i]);
                new_wave.push(wave[i]);
            }
        }
        source.data = {'date': new_dates, 'wind_speed': new_wind_speed, 'wave': new_wave};
        source.change.emit();
        
        //Added by Christine : make an ajax call to send to the server the slider.value  (with the request param 'chosen_date')
        #https://stackoverflow.com/questions/50853416/how-to-trigger-ajax-call-after-a-box-selection-is-done-in-python-bokeh-plot
        (function($){
            $.getJSON('/ajaxviz', {
                chosen_date: slider.value,
                }, function(data) {
                    $('#date-param').html(data.html_plot);
            })
        })(jQuery);
    """)
                  

    slider.js_on_change('value', callback)
    layout = column(slider, p)

    #show(layout)
    
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    script, div = components(layout)

    return render_template(
        'dunkerque.html',
        p_script=script,
        p_div=div,
        p_msg=msg,
        js_resources=js_resources,
        css_resources=css_resources,
    )

if __name__ == '__main__':
    # change the current directory
    # to specified directory
    os.chdir(r"C:\Travail\Enseignement\Cours_M2_python\Projet_Elenie")
    print(os.getcwd())
    app.run(debug=True, port=5050)
