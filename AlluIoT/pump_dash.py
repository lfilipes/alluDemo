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
from datetime import datetime
from flask_login import login_required
import os

def Add_Dash(server):

    def protect_dashviews(dashapp):
         for view_func in dashapp.server.view_functions:
            if view_func.startswith(dashapp.url_base_pathname):
                dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])

    dashapp = dash.Dash(__name__, server=server, url_base_pathname='/pump_dash/', external_stylesheets=[dbc.themes.BOOTSTRAP])
    protect_dashviews(dashapp)
    server = dashapp.server 
    
    ####
    # Cria os dados para as tensões das bombas
    # time stamps for consumprion each 6 hours
    ####
    
    date_rngCons = pd.date_range(start = '2019 JAN 01 00:00:01', end = '2019 APR 30 00:39:01', freq = '6H')
    dfC = pd.DataFrame(pd.to_datetime(date_rngCons), columns = ['ts'])
    dfC = dfC.set_index('ts')

    # Reservoir value each 6 hours minutes 
    dfC['V_Pump1Ete1'] = np.random.randint(low=108, high=112, size=len(date_rngCons))
    dfC['V_Pump1Ete2'] = np.random.randint(low=107, high=113, size=len(date_rngCons))
    dfC['V_Pump1Ete3'] = np.random.randint(low=109, high=111, size=len(date_rngCons))
    
    ####
    # inicio preenche option box com tuple estática
    ####

    body = dbc.Container(
        [
            dbc.Row(dbc.Col(html.Div(html.H2('Dashboard da Tensão nas Bombas das ETEs')))),
            dbc.Row(
                [
               
                   dbc.Col(
                        [
                            html.H3('INÍCIO / FIM:'),
                                dcc.DatePickerRange(
                                    id='my_date_picker',
                                    min_date_allowed=datetime(2018, 10, 1),
                                    max_date_allowed=datetime.today(),
                                    start_date=datetime(2018, 12, 1),
                                    end_date=datetime.today()
                                )
                        ],
                        md=6,
                    ),
                            
                ]
            ),

       dbc.Row(
                [
                   dbc.Col(
                        [
                            html.Button(
                                id='submit-button',
                                n_clicks=0,
                                children='Submit',
                            ),
                        ],
                        md=4,
                    ),
                ]
            ),

            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(
                                id='Pump1Ete1',
                                figure={
                                    'data': [
                                        {'x': [1, 2, 3], 'y': [110, 111, 112], 'type': 'Scatter', 'mode':'lines', 'name': 'Bomba1_ETE1'},
                                    ]
                                }
                            )
                        ],
                        md=12,
                    ),
                ]
            ),

            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(
                                id='Pump1Ete2',
                                figure={
                                    'data': [
                                        {'x': [1, 2, 3], 'y': [110, 111, 112], 'type': 'Scatter', 'mode':'lines', 'name': 'Bomba1_ETE2'},
                                    ]
                                }
                            )
                        ],
                        md=12,
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(
                                id='Pump1Ete3',
                                figure={
                                    'data': [
                                        {'x': [1, 2, 3], 'y': [110, 111, 112], 'type': 'Scatter', 'mode':'lines', 'name': 'Bomba1_ETE3'},
                                    ]
                                }
                            )
                        ],
                        md=12,
                    ),
                ]
            ),
        ],
        className="mt-4",fluid=True,
    )

    dashapp.layout =  html.Div([body]) 



    @dashapp.callback(
        Output('Pump1Ete1', 'figure'),
        [Input('submit-button', 'n_clicks')],
        [State('my_date_picker', 'start_date'),
        State('my_date_picker', 'end_date')])

    def update_graphPump1(n_clicks, start_date, end_date):
        start = datetime.strptime(start_date[:10], '%Y-%m-%d')
        end = datetime.strptime(end_date[:10], '%Y-%m-%d')
        traces = []
        df = pd.DataFrame(index=dfC.index.copy())
        df = dfC['V_Pump1Ete1'].copy()
        df = df.loc[start:end]
        traces.append({'x':df.index, 'y':df.values, 'type':'Scatter', 'mode':'lines', 'name':'Bomba_1 Ete_1'})

        fig = {
            'data': traces,
            'layout': {'title':'Tesão: Bomaba 1 da ETE 1',
                'yaxis':{'range':[100,115],'autorange':False, 'title':'Tensão Volts'},
                'xaxis': {'title':'Período de Tempo'},
                'shapes': [
                    {
                        'type': 'line',
                        'xref': 'paper',
                        'x0': 0,
                        'y0': 110.0,
                        'x1': 1,
                        'y1': 110.0,
                        'line':{
                            'color': 'rgb(255, 0, 0)',
                            'width': 4,
                            'dash':'dot'
                        }
                    }
                ]
            }
        }
        return fig

    @dashapp.callback(
        Output('Pump1Ete2', 'figure'),
        [Input('submit-button', 'n_clicks')],
        [State('my_date_picker', 'start_date'),
        State('my_date_picker', 'end_date')])

    def update_graphPump2(n_clicks, start_date, end_date):
        start = datetime.strptime(start_date[:10], '%Y-%m-%d')
        end = datetime.strptime(end_date[:10], '%Y-%m-%d')
        traces = []
        df = pd.DataFrame(index=dfC.index.copy())
        df = dfC['V_Pump1Ete2'].copy()
        df = df.loc[start:end]
        traces.append({'x':df.index, 'y':df.values, 'type':'Scatter', 'mode':'lines', 'name':'Bomba_1 Ete_2'})

        fig = {
            'data': traces,
            'layout': {'title':'Tesão: Bomaba 1 da ETE 2',
                'yaxis':{'range':[100,115],'autorange':False, 'title':'Tensão Volts'},
                'xaxis': {'title':'Período de Tempo'},
                'shapes': [
                    {
                        'type': 'line',
                        'xref': 'paper',
                        'x0': 0,
                        'y0': 110.0,
                        'x1': 1,
                        'y1': 110.0,
                        'line':{
                            'color': 'rgb(255, 0, 0)',
                            'width': 4,
                            'dash':'dot'
                        }
                    }
                ]
            }
        }
        return fig

    @dashapp.callback(
        Output('Pump1Ete3', 'figure'),
        [Input('submit-button', 'n_clicks')],
        [State('my_date_picker', 'start_date'),
        State('my_date_picker', 'end_date')])

    def update_graphPump3(n_clicks, start_date, end_date):
        start = datetime.strptime(start_date[:10], '%Y-%m-%d')
        end = datetime.strptime(end_date[:10], '%Y-%m-%d')
        traces = []
        df = pd.DataFrame(index=dfC.index.copy())
        df = dfC['V_Pump1Ete3'].copy()
        df = df.loc[start:end]
        traces.append({'x':df.index, 'y':df.values, 'type':'Scatter', 'mode':'lines', 'name':'Bomba_1 Ete_3'})

        fig = {
            'data': traces,
            'layout': {'title':'Tesão: Bomaba 1 da ETE 3',
                'yaxis':{'range':[100,115],'autorange':False, 'title':'Tensão Volts'},
                'xaxis': {'title':'Período de Tempo'},
                'shapes': [
                    {
                        'type': 'line',
                        'xref': 'paper',
                        'x0': 0,
                        'y0': 110.0,
                        'x1': 1,
                        'y1': 110.0,
                        'line':{
                            'color': 'rgb(255, 0, 0)',
                            'width': 4,
                            'dash':'dot'
                        }
                    }
                ]
            }
        }
        return fig

    return dashapp.server