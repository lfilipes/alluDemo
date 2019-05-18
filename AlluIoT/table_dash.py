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

    dashapp = dash.Dash(__name__, server=server, url_base_pathname='/tab_dash/', external_stylesheets=[dbc.themes.BOOTSTRAP])
    protect_dashviews(dashapp)
    server = dashapp.server 

    ####
    # Cria os dados para aa caixas dágua
    ####
    # time stamps for consumprion
    date_rngCons = pd.date_range(start = '2019 JAN 1 00:00:01', end = '2019 DEC 31 23:59:59', freq = '360T')
    df = pd.DataFrame(pd.to_datetime(date_rngCons), columns = ['ts'])
    df = df.set_index('ts')
    df['time_stamp'] = date_rngCons
    # volume each 15 minutes
    df['Ete_1'] = np.random.randint(low=0, high=4, size=len(date_rngCons))
    df['Ete_2'] = np.random.randint(low=1, high=5, size=len(date_rngCons))
    df['Ete_3'] = np.random.randint(low=1, high=6, size=len(date_rngCons))

    startdate = pd.to_datetime('2019 JAN 1 00:00:01').date()
    enddate = pd.to_datetime('2019 JAN 31 23:59:59').date()
    df1=df.loc[startdate:enddate]

    def get_df(m):
        if   m == 1:
            return  df1
        elif m == 2:
            return  df.loc[pd.to_datetime('2019 FEB 1 00:00:01').date():pd.to_datetime('2019 FEB 28 23:59:59').date()]
        elif m == 3:
            return  df.loc[pd.to_datetime('2019 MAR 1 00:00:01').date():pd.to_datetime('2019 MAR 31 23:59:59').date()]
        elif m == 4:
            return  df.loc[pd.to_datetime('2019 APR 1 00:00:01').date():pd.to_datetime('2019 APR 30 23:59:59').date()]
        elif m == 5:
            return  df.loc[pd.to_datetime('2019 MAY 1 00:00:01').date():pd.to_datetime('2019 MAY 31 23:59:59').date()]
        elif m == 6:
            return  df.loc[pd.to_datetime('2019 JUN 1 00:00:01').date():pd.to_datetime('2019 JUN 30 23:59:59').date()]
        elif m == 7:
            return  df.loc[pd.to_datetime('2019 JUL 1 00:00:01').date():pd.to_datetime('2019 JUL 31 23:59:59').date()]
        elif m == 8:
            return  df.loc[pd.to_datetime('2019 AUG 1 00:00:01').date():pd.to_datetime('2019 AUG 31 23:59:59').date()]
        elif m == 9:
            return  df.loc[pd.to_datetime('2019 SEP 1 00:00:01').date():pd.to_datetime('2019 SEP 30 23:59:59').date()]
        elif m == 10:
            return  df.loc[pd.to_datetime('2019 OCT 1 00:00:01').date():pd.to_datetime('2019 OCT 31 23:59:59').date()]
        elif m == 11:
            return  df.loc[pd.to_datetime('2019 NOV 1 00:00:01').date():pd.to_datetime('2019 NOV 30 23:59:59').date()]
        elif m == 12:
            return  df.loc[pd.to_datetime('2019 DEC 1 00:00:01').date():pd.to_datetime('2019 DEC 31 23:59:59').date()]
            
    ####
    # inicio preenche option box com tuple e
    ####
    options=[{"label":'Ete_1',"value":'Ete_1'},{"label":'Ete_2',"value":'Ete_2'},
        {"label":'Ete_3',"value":'Blobo_3'},]


    body = dbc.Container(
        [
            dbc.Row(dbc.Col(html.Div(html.H2('Níveis das ETEs Mês-a-Mês')))),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3('Selecione o Mes que Deseja Visualizar'),
                            dcc.Slider(
                                id='month-slider',
                                min=1,
                                max=12,
                                value=1,
                                marks={
                                    1: 'JAN', 
                                    2: 'FEB', 
                                    3: 'MAR', 
                                    4: 'APR', 
                                    5: 'MAY', 
                                    6: 'JUN', 
                                    7: 'JUL', 
                                    8: 'AUG', 
                                    9: 'SEP', 
                                    10: 'OCT', 
                                    11: 'NOV', 
                                    12: 'DEC', 
                                }
                            )
                        ],
                        md=12,
                    ),              
                    
                ]
            ),
       dbc.Row(dbc.Col(html.Div(id='updatemode-output-container'))), 
       dbc.Row(
                [
                   dbc.Col(
                        [
                            dash_table.DataTable(
                                id='datatable',
                                columns=[
                                {"name": i, "id": i, "deletable": False} for i in df1.columns
                                ],
                                data=df1.to_dict("rows"),
                                editable=True,
                                filtering=True,
                                sorting=True,
                                sorting_type="multi",
                                row_selectable="multi",
                                row_deletable=False,
                                selected_rows=[],
                                pagination_mode="fe",
                                    pagination_settings={
                                        "displayed_pages": 1,
                                        "current_page": 0,
                                        "page_size": 35,
                                    },
                                    navigation="page",
                            ),
                        ],
                        md=12,
                    ),
                ]
            ),
        dbc.Row(dbc.Col(html.Div(id='datatable-interactivity-container'))), 
        ],
        className="mt-4",fluid=True,
    )

    dashapp.layout =  html.Div([body]) 

    @dashapp.callback(
        Output('datatable', "data"),
        [Input('month-slider' , 'value')])
    def update_table_data(value):
        dfn = get_df(value)
        data = dfn.to_dict("rows")
        
        return data

    @dashapp.callback(
        Output('datatable', "columns"),
        [Input('month-slider' , 'value')])
    def update_table_columns(value):
        dfn = get_df(value)
        columns =[{"name": i, "id": i} for i in dfn.columns]
        
        return columns

    @dashapp.callback(
        Output('datatable-interactivity-container', "children"),
        [Input('datatable', "derived_virtual_data"),
        Input('datatable', "derived_virtual_selected_rows"),
        Input('month-slider' , "value")])
    def update_graph(rows, derived_virtual_selected_rows, value):

        if derived_virtual_selected_rows is None:
            derived_virtual_selected_rows = []
        
        if rows is None:
            dfn = get_df(value)
        else:
            dfn = pd.DataFrame(rows)

        colors = []
        for i in range(len(dfn)):
            if i in derived_virtual_selected_rows:
                colors.append("#7FDBFF")
            else:
                colors.append("#0074D9")

        return html.Div(
            [
                dcc.Graph(
                    id=column,
                    figure={
                        "data": [
                            {
                                "x": dfn["time_stamp"],
                                # check if column exists - user may have deleted it
                                # If `column.deletable=False`, then you don't
                                # need to do this check.
                                "y": dfn[column] if column in dfn else [],
                                "type": "bar",
                                "marker": {"color": colors},
                            }
                        ],
                        "layout": {
                            "xaxis": {"automargin": True},
                            "yaxis": {"automargin": True},
                            "height": 250,
                            "margin": {"t": 10, "l": 10, "r": 10},
                        },
                    },
                )
                for column in ["Ete_1", "Ete_2", "Ete_3"]
            ]
        )

    return dashapp.server