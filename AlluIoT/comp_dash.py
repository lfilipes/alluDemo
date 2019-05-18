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

    dashapp = dash.Dash(__name__, server=server, url_base_pathname='/comp_dash/', external_stylesheets=[dbc.themes.BOOTSTRAP])
    protect_dashviews(dashapp)
    server = dashapp.server 
    
    ####
    # Cria os dados para a sala 001
    ####
    # time stamps for consumprion
    date_rngCons = pd.date_range(start = '2018 JAN 01 00:00:01', end = '2019 APR 30 00:39:01', freq = 'D')
    dfC = pd.DataFrame(pd.to_datetime(date_rngCons), columns = ['ts'])
    dfC = dfC.set_index('ts')
    # Eteoir value each 30 minutes 
    dfC['Ete_1'] = np.random.randint(low=1, high=3, size=len(date_rngCons))
    dfC['Ete_2'] = np.random.randint(low=1, high=4, size=len(date_rngCons))
    dfC['Ete_3'] = np.random.randint(low=1, high=5, size=len(date_rngCons))
    
    ####
    # inicio preenche option box com tuple estática
    ####
    options=[{"label":'ETE_1',"value":'Ete_1'},{"label":'ETE_2',"value":'Ete_2'},
        {"label":'ETE_3',"value":'Ete_3'}]


    body = dbc.Container(
        [
            dbc.Row(dbc.Col(html.Div(html.H2('Volume das ETEs')))),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3('Escolha a ETE:'),
                            dcc.Dropdown(
                                id='my_Ete_picker',
                                options=options,
                                value=['Ete_1'],
                                multi=True
                            )
                        ],
                        md=6,
                    ),
                   
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
                                id='my_graph',
                                
                                figure={
                                    'data': [
                                        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'Scatter', 'mode':'lines', 'name': 'Ete_1'},
                                        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'Scatter', 'mode':'lines', 'name': 'Ete_2'},
                                        {'x': [1, 2, 3], 'y': [3, 3, 3], 'type': 'Scatter', 'mode':'lines', 'name': 'Ete_3'}
                                    ]
                                },config={'staticPlot': True}
                            )
                        ],
                        md=12,
                    ),
                ]
            )
        ],
        className="mt-4",fluid=True,
    )

    dashapp.layout =  html.Div([body]) 
# ,style={'width':'480px',}

    @dashapp.callback(
        Output('my_graph', 'figure'),
        [Input('submit-button', 'n_clicks')],
        [State('my_Ete_picker', 'value'),
        State('my_date_picker', 'start_date'),
        State('my_date_picker', 'end_date')])

    def update_graph(n_clicks, Ete_pick, start_date, end_date):
        start = datetime.strptime(start_date[:10], '%Y-%m-%d')
        end = datetime.strptime(end_date[:10], '%Y-%m-%d')
        traces = []
        df = pd.DataFrame(index=dfC.index.copy())
        for Ete in Ete_pick:
            df[Ete] = dfC[[Ete]].copy()
            df = df.loc[start:end]
            traces.append({'x':df.index, 'y':df[Ete].values, 'type':'Scatter', 'mode':'lines', 'name':Ete})

        fig = {
            'data': traces,
            'layout': {'title':'Nivel da ETE (1-Minimo / 5-Transbordo)',
                'yaxis':{'range':[0,5],'autorange':False, 'title':'Nivel (0 - 5)'},
                'xaxis': {'title':'Período de Tempo'},
#                'autosize':True,
#                'width':900,
#                'height':600
            }
        }

        return fig

    return dashapp.server