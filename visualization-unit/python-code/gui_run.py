from dash import Dash, dcc, html, Input, Output, callback
import pandas
import sqlite3
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import os
import webbrowser
from threading import Timer

#create app layout
#multi-tab layout to use on 5" touchscreen
#avoid having to scroll to view content
app = Dash()

app.layout = html.Div([
    html.Div(
        html.H1('MU AIR: Display Your Local Air Quality')
    ),
    dcc.Tabs(id="tabs", value='tab-ataglance', children=[
        dcc.Tab(label='At A Glance', id='tabs-glance', value='tab-ataglance', children=[
        ]),

        dcc.Tab(label='Graphs', id='tabs-graph', value='tabs-anygraph', children=[
        ]),

    ]),
#interval to update all figures
    dcc.Interval(id='interval_component',
            interval=1500*1000
            ),
    html.Div(id='tabs-show'
    ),
])

#Callbacks
#'At a Glance' tab
@app.callback(Output('tabs-glance', 'children'),
              Input('tabs', 'value'),
              Input('interval_component','n_intervals'),
              )

def update_tabs(value, n_intervals):
#fetch single latest value for instant temp/humidity/aqi display
    conn=sqlite3.connect('MUAIRtestdatabase', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT avg FROM temp ORDER BY rowid DESC LIMIT 1")
    tempvalue, = cursor.fetchone()
    cursor.execute("SELECT avg FROM humidity ORDER BY rowid DESC LIMIT 1")
    humidityvalue, = cursor.fetchone()

#section for all the figures
#humidity and temp
    fighumidity = go.Figure()
    fighumidity.add_trace(go.Indicator(
            mode = "number+gauge",
            value = tempvalue,
            domain = {'x': [0.25, 1], 'y': [0.4, 0.6]},
            title = {'text': "Temperature", 'font':{'size': 25}},
            number={'suffix': "°F", 'font': {'size': 35}},
            gauge = {
                'shape': "bullet",
                'axis': {'range': [-30, 120]},
                'threshold': {
                    'line': {'color': "lightblue", 'width': 6},
                    'thickness': 1,
                    'value': -20},
                'bar':
                    {'color': "darkred", 'thickness': .8}
                    }))
    fighumidity.add_trace(go.Indicator(
        mode = "number+gauge",
        value = humidityvalue,
        domain = {'x': [0.25, 1], 'y': [0.0, 0.2]},
        title = {'text': "Humidity", 'font':{'size': 25}},
        number={'suffix': "%", 'font': {'size': 35}},
        gauge = {
            'shape': "bullet",
            'axis': {'range': [0, 100]},
            'bar': {'color': "blue", 'thickness': 0.8}}))

#AQI
    cursor.execute("SELECT aqi10 FROM aqi10 ORDER BY rowid DESC LIMIT 1")
    aqi10data, = cursor.fetchone()
    cursor.execute("SELECT aqi25 FROM aqi25 ORDER BY rowid DESC LIMIT 1")
    aqi25data, = cursor.fetchone()

    if aqi10data > aqi25data:
        aqidata=aqi10data
    elif aqi25data > aqi10data:
        aqidata=aqi25data
    elif aqi10data == aqi25data:
        aqidata=aqi10data

    if 0 <= aqidata <= 50:
        barcolor = 'lightgreen'
    elif 51 <= aqidata <= 100:
        barcolor = 'yellow'
    elif 101 <= aqidata <= 150:
        barcolor = 'orange'
    elif 151 <= aqidata <= 200:
        barcolor = 'red'
    elif 201 <= aqidata <= 300:
        barcolor = 'purple'
    elif 301 <= aqidata:
        barcolor = 'darkred'
    else :
        pass
    figaqi = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = aqidata,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "AQI", 'font': {'size': 45}},
        gauge = {
            'axis': {'range': [None, 400], 'tickwidth': 1, 'tickcolor': "black"},
            'bar': {'color': barcolor},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 400], 'color': 'lightblue'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 301}}))
    figaqi.update_layout(font = {'color': "black", 'family': "Arial", 'size': 30})
    if value == 'tab-ataglance':
        return html.Div([
            html.H1([dcc.Graph(figure=figaqi, style={'display': 'inline-block', 'width': '40vw', 'height': '80vh'}),
                    dcc.Graph(figure=fighumidity, style={'display': 'inline-block','width': '50vw', 'height': '75vh'})]),
        ])




#Create layered tabs for histographs
@app.callback(Output('tabs-graph','children'),
              Input('tabs','value'),
              Input('interval_component','n_intervals'),
              )

#create smaller tabs, each with graph
def update_tabs(value,n_intervals):
#PM-----------------------------------------------------------------------------------------------------
    figpm = go.Figure()
    #connect to database
    conn=sqlite3.connect('MUAIRtestdatabase', check_same_thread=False)
    #figure creation def
    def update_fig(n_intervals,particle):
        #connect to dataframe
        dfpm= pandas.read_sql_query("SELECT * FROM totalpm", conn)
        figpm=px.line( dfpm,x='time', y='avg', color='particle', line_shape="linear")
        #display updated figure
        return figpm
    figpm.update_layout(
        title_text="Particulate Matter Histograph"
    )
#create individual PM graphs
    figpm1 = go.Figure()
    figpm25 = go.Figure()
    figpm4 = go.Figure()
    figpm10 = go.Figure()
#connect to database and create base figure
    conn=sqlite3.connect('MUAIRtestdatabase', check_same_thread=False)
    dfpm1= pandas.read_sql_query("SELECT * FROM pm1", conn)
    dfpm25= pandas.read_sql_query("SELECT * FROM pm2p5", conn)
    dfpm4= pandas.read_sql_query("SELECT * FROM pm4", conn)
    dfpm10= pandas.read_sql_query("SELECT * FROM pm10", conn)
#pm1----------
    figpm1=px.line( dfpm1,x='time', y='avg', line_shape="linear")
    figpm1.update_layout(
        title_text="PM1"
    )
    # Add range slider
    figpm1.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7,
                        label="1w",
                        step="day",
                        stepmode="backward"),
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
#pm2.5----
    figpm25=px.line( dfpm25,x='time', y='avg', line_shape="linear")
    figpm25.update_layout(
        title_text="PM2.5"
    )
    # Add range slider
    figpm25.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7,
                        label="1w",
                        step="day",
                        stepmode="backward"),
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
#pm4----
    figpm4=px.line( dfpm4,x='time', y='avg', line_shape="linear")
    figpm4.update_layout(
        title_text="PM4"
    )
    # Add range slider
    figpm4.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7,
                        label="1w",
                        step="day",
                        stepmode="backward"),
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
#pm10-----
    figpm10=px.line( dfpm10,x='time', y='avg', line_shape="linear")
    figpm10.update_layout(
        title_text="PM10"
    )
    # Add range slider
    figpm10.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7,
                        label="1w",
                        step="day",
                        stepmode="backward"),
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )


#NOX--------------------------------------------------------------------------------------------------
    fignox = go.Figure()
#connect to database and create base figure
    conn=sqlite3.connect('MUAIRtestdatabase', check_same_thread=False)
    dfnox= pandas.read_sql_query("SELECT * FROM nox", conn)
    fignox=px.line( dfnox,x='time', y='avg', line_shape="linear")
    fignox.update_layout(
        title_text="NOX Index Histograph"
    )
# Add range slider
    fignox.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7,
                        label="1w",
                        step="day",
                        stepmode="backward"),
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )


#VOC---------------------------------------------------------------------------------------------------
    figvoc = go.Figure()
#connect to database and create figure
    conn=sqlite3.connect('MUAIRtestdatabase', check_same_thread=False)
    dfvoc= pandas.read_sql_query("SELECT * FROM voc", conn)
    figvoc=px.line( dfvoc,x='time', y='avg', line_shape="linear")
    figvoc.update_layout(
        title_text="VOC Index Histograph"
    )
# Add range slider
    figvoc.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7,
                        label="1w",
                        step="day",
                        stepmode="backward"),
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True,
            ),
            type="date"
        )
    )

#if the graphs tab is selected...return certain graphs based on sub graphs
    if value == 'tabs-anygraph':
        return dcc.Tabs(id='graph-tabs', value='PM1Graph', children=[
            dcc.Tab(label='Particulate Matter: PM1', id='pm1graph', value='PM1Graph', children=[
                html.Div(
                    html.H1(dcc.Graph(figure=figpm1, id='figpm1graph')))
            ]),
            dcc.Tab(label='Particulate Matter: PM2.5', id='pm25graph', value='PM25Graph', children=[
                html.Div(
                    html.H1(dcc.Graph(figure=figpm25, id='figpm25graph')))
            ]),
            dcc.Tab(label='Particulate Matter: PM4', id='pm4graph', value='PM4Graph', children=[
                html.Div(
                    html.H1(dcc.Graph(figure=figpm4, id='figpm4graph')))
            ]),
            dcc.Tab(label='Particulate Matter: PM10', id='pm10graph', value='PM10Graph', children=[
                html.Div(
                    html.H1(dcc.Graph(figure=figpm10, id='figpm10graph')))
            ]),
            dcc.Tab(label='NOX Index', id='noxgraph', value='NOXGraph',  children=[
                html.Div(
                    html.H1(dcc.Graph(figure=fignox, id='fignoxgraph')))
            ]),
            dcc.Tab(label='VOC Index', id='vocgraph', value='VOCGraph',  children=[
                html.Div([
                    html.H1(dcc.Graph(figure=figvoc, id='figvocgraph')
                            ),

            ])
            ])
        ])

#def main():
#    if not os.environ.get("gui_run"):
#        print("ope")
#        #webbrowser.open_new('http://127.0.0.1:8050')
#        #os.system("chromium-browser --start-fullscreen http://127.0.0.1:8050")

#    app.run(host="127.0.0.1", port=8050)

#debug app, eventually will be deploying app
#if __name__ == '__main__':
    #Timer(600000, main).start()
    #app.run(port=8050)
#    main()


if __name__ == '__main__':
    app.run()