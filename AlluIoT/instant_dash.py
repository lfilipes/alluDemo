import glob
import dash_table
from datetime import datetime
import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas_datareader as pdr
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from plotly.graph_objs import *
import pandas_datareader as pdr
import pandas_datareader.data as web # requires v0.6.0 or later
import pandas as pd
import numpy as np
import dash_daq as daq
from datetime import datetime
from flask_login import login_required
import os

def Add_Dash(server):

    def protect_dashviews(dashapp):
         for view_func in dashapp.server.view_functions:
            if view_func.startswith(dashapp.url_base_pathname):
                dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])
       
    dashapp = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP], url_base_pathname='/instant_dash/', static_folder='static')
    protect_dashviews(dashapp)
    server = dashapp.server 

    @dashapp.server.route('/static/<path>')
    def static_file(path):
        static_folder = os.path.join(os.getcwd(), 'static')
        return send_from_directory(static_folder, path)

    body1 = dbc.Container(
            [
                dbc.Row(dbc.Col(html.Div(html.H2('Volume Instantâneo das ETEs')))),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                daq.Tank(
                                    label='ETE #1',
                                    id='tank_1',
                                    units="Vol H2O",
                                    style={'margin-left': '50px'},
                                    showCurrentValue=True,
                                    max=5,
                                    min=0,
                                    value=2
                                ),
                                html.P('',style={'padding':'2em 0 0 2em'}),
                                dcc.Slider(
                                    id='tank_1-slider',
                                    min=0,
                                    max=5,
                                    step=1,
                                    value=2
                                ),
                            ],
                            md=4,
                        ), 
                        dbc.Col(
                            [
                                daq.Tank(
                                    label='ETE #2',
                                    id='tank_2',
                                    style={'margin-left': '50px'},
                                    showCurrentValue=True,
                                    units="Vol H2O",
                                    max=5,
                                    min=0,
                                    value=3
                                ),
                                html.P('',style={'padding':'2em 0 0 2em'}),
                                dcc.Slider(
                                    id='tank_2-slider',
                                    min=0,
                                    max=5,
                                    step=1,
                                    value=3
                                ),      
                            ],
                            md=4,
                        ),                       
                        dbc.Col(
                            [
                                daq.Tank(
                                    label='ETE #3',
                                    id='tank_3',
                                    style={'margin-left': '50px'},
                                    showCurrentValue=True,
                                    units="Vol H2O",
                                    max=5,
                                    min=0,
                                    value=4
                                ),
                                html.P('',style={'padding':'2em 0 0 2em'}),
                                dcc.Slider(
                                    id='tank_3-slider',
                                    min=0,
                                    max=5,
                                    step=1,
                                    value=4
                                ),     
                            ],
                            md=4,
                        ),   
                    ]
                ),
            ],
            className="mt-4",fluid=True,
        )

    body2 = dbc.Container(
            [   
                dbc.Row(dbc.Col(html.Div(html.H2('Status das Bombas')))),
                dbc.Row(
                    [
                    dbc.Col(
                            [
                                daq.LEDDisplay(
                                    label="Bomba A / ETE #1",
                                    value='110.00',
                                    backgroundColor="#007acc"
                                ),
                                html.P('',style={'padding':'2em 0 0 2em'}),
                                daq.PowerButton(
                                    on='True',
                                    theme='dark',
                                    color="#009933"
                                ),
                            ],
                            md=4,
                        ),
                        dbc.Col(
                            [
                                daq.LEDDisplay(
                                    label="Bomba A / ETE #2",
                                    value='110.00',
                                    backgroundColor="#007acc"
                                ),
                                html.P('',style={'padding':'2em 0 0 2em'}),
                                daq.PowerButton(
                                    on='True',
                                    color="#009933"
                                ),
                            ],
                            md=4,
                        ),
                        dbc.Col(
                            [
                                daq.LEDDisplay(
                                    label="Bomba A / ETE #3",
                                    value='110.00',
                                    backgroundColor="#007acc"
                                ),
                                html.P('',style={'padding':'2em 0 0 2em'}),
                                daq.PowerButton(
                                    on='True',
                                    color="#009933"
                                ),
                            ],
                            md=4,
                        ),
                    ]
                ),
            ],
            className="mt-4",fluid=True,
        )

    dashapp.layout =  html.Div([body1,body2]) 
  
### Tanks
    @dashapp.callback(
        dash.dependencies.Output('tank_1', 'value'),
        [dash.dependencies.Input('tank_1-slider', 'value')]
    )
    def update_output_4(value):
        return value

    @dashapp.callback(
        dash.dependencies.Output('tank_2', 'value'),
        [dash.dependencies.Input('tank_2-slider', 'value')]
    )
    def update_output_5(value):
        return value 

    @dashapp.callback(
    dash.dependencies.Output('tank_3', 'value'),
    [dash.dependencies.Input('tank_3-slider', 'value')]
    )
    def update_output_6(value):
        return value

    return dashapp.server