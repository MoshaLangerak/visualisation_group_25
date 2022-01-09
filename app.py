from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.data import create_districts_df, merge_df, stats_per_capita, load_accident_data, load_population_data, load_geojson_data, create_districts_dates_df, create_date_df

import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go


if __name__ == '__main__':
    # ----------------------- Loading & preprocessing data -------------------------------
    # Create data
    file_path_1 = 'Data/all_years_2000_2020.csv'
    file_path_2 = 'Data/Population data 2018.csv'
    file_path_geojson = 'Data/uk_local_areas/uk_la.geojson'

    stats = ['Accident Severity', 'Number of vehicles', 'Number of casualties']
    token = 'pk.eyJ1IjoibW9zaGEtbGFuZ2VyYWsiLCJhIjoiY2t3ZGoxMmtxMGt2ZzJudDN5NXA0YWQ4ciJ9.6QIBuYFeAajMhniiNVU-GA'
    statistics = ['Accident Severity', 'Number of vehicles', 'Number of casualties', 'Accident Severity Per capita', 'Number of vehicles Per capita', 'Number of casualties Per capita']

    print('Loading data...')
    df_pd = load_accident_data(file_path_1)
    df_pop = load_population_data(file_path_2)
    print('Creating district data...')
    df_grouped = create_districts_df(df_pd)
    df_districts = merge_df(df_grouped, df_pop)
    stats_per_capita(df_districts, stats)
    print('Loading GeoJSON data...')
    geojson = load_geojson_data(file_path_geojson)
    print('Creating date data...')
    df_districts_dates = create_districts_dates_df(df_pd)
    df_dates = create_date_df(df_pd)
    
    # ----------------------- Initializing options for the interactions --------------------
    #dropdown options (for features)
    available_indicators = df_dates[['nr_accidents_pd', 'nr_vehicles_pd', 'nr_casualties_pd']] #add here all the column names/variables we want to use in the dropdown menu
    opts = [{'label': 'Number of accidents', 'value': 'nr_accidents_pd'},
            {'label': 'Number of vehicles in an accident', 'value': 'nr_vehicles_pd'},
            {'label': 'Number of casualties', 'value': 'nr_casualties_pd'}]

    #second dropdown options (for districts)
    available_indicators2 = df_districts_dates['local_authority_district'].sort_values()
    opts2 = [{'label': i, 'value': i} for i in available_indicators2.unique()]

    #range slider options
    dates = ['2000-01-01', '2001-01-01', '2002-01-01', '2003-01-01', '2004-01-01',
            '2005-01-01', '2006-01-01', '2007-01-01', '2008-01-01', '2009-01-01',
            '2010-01-01', '2011-01-01', '2012-01-01', '2013-01-01', '2014-01-01',
            '2015-01-01', '2016-01-01', '2017-01-01', '2018-01-01', '2019-01-01',
            '2020-01-01', '2020-12-31']

    # ----------------------- Initializing starting figure -------------------------------
    fig_1 = px.choropleth_mapbox(
            df_districts, geojson=geojson, color=statistics[0],
            locations='Local Authority District Code', featureidkey= 'properties.geo_code',
            mapbox_style='dark')
    fig_1.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0},
            mapbox_zoom=4.3, # use this to zoom in on the map
            mapbox_center_lat = 54.5, # use this to align the map on latitude
            mapbox_center_lon = -3, # use this to align the map on longitude
            mapbox_accesstoken=token, # token used for getting a different map type
            width=800,
            height=750)
    
    #creating a figure
    trace_1 = go.Scatter(x = df_dates['date'], y = df_dates['nr_accidents_pd'],
                        name = 'nr_accidents_pd',
                        line = dict(width = 2,
                                    color = 'rgb(106, 181, 135)')) #green if no district selected
    layout = go.Layout(title = 'Distribution of the number of accidents, vehicles and casualties over time',
                    hovermode = 'closest')
    fig_2 = go.Figure(data = [trace_1], layout = layout)

    # ----------------------- Dash(board) lay-out ----------------------------------------
    app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
        
    # app.layout = html.Div(
    #     id='app-container',
    #     children=[
    #         html.Div([
    #             html.H1('Road safety dashboard'),
    #             html.P('Welcome to the road safety dashboard')
    #                     ],
    #                 style = {'padding' : '50px' ,
    #                         'backgroundColor' : '#3aaab2'}),
    #              # dropdown
    #             html.P([
    #                 html.Label('Choose a feature'),
    #                 dcc.Dropdown(id = 'stat', 
    #                                 options = [{'value': x, 'label': x} for x in statistics],
    #                                 value = statistics[0])
    #                     ], style = {'width': '400px',
    #                                 'fontSize' : '20px',
    #                                 'display': 'inline-block'}),
                
    #             dcc.Graph(id='choropleth', figure = fig_1),
    #             # adding a plot
    #             dcc.Graph(id = 'plot', figure = fig_2),
    #             # dropdown for features
    #             html.P([
    #                 html.Label('Choose a feature'),
    #                 dcc.Dropdown(id = 'opt', options = opts,
    #                             value = opts[0], multi=False)
    #                     ], style = {'width': '400px',
    #                                 'fontSize' : '20px',
    #                                 'padding-left' : '100px',
    #                                 'display': 'inline-block'}),
    #             #dropdown for districts
    #             html.P([
    #                 html.Label('Choose a district'),
    #                 dcc.Dropdown(id = 'opt2', options = opts2,
    #                              multi=False)
    #                     ], style = {'width': '400px',
    #                                 'fontSize' : '20px',
    #                                 'padding-left' : '100px',
    #                                 'display': 'inline-block'}),
    #             # range slider
    #             html.P([
    #                 html.Label('Time Period'),
    #                 dcc.RangeSlider(id = 'slider',
    #                                 marks = {i: 2000+i for i in range(0,22)},
    #                                 min = 0,
    #                                 max = 21,
    #                                 value = [0,21])
    #                     ], style = {'width' : '80%',
    #                                 'fontSize' : '20px',
    #                                 'padding-left' : '100px',
    #                                 'display': 'inline-block'})
    #     ]
    # )
    
    
    app.layout = html.Div(
        [
        dbc.Row(dbc.Col(html.Div("Title"), style = {'padding' : '50px' , 'backgroundColor' : '#3aaab2'})),
        dbc.Row(
            [
                dbc.Col(html.Div(html.P([
                    html.Label('Choose a feature'),
                    dcc.Dropdown(id = 'stat', 
                                    options = [{'value': x, 'label': x} for x in statistics],
                                    value = statistics[0])
                        ])), width=4),
                dbc.Col(html.Div(dcc.Graph(id='choropleth', figure = fig_1)), width=8),
            ]),
        dbc.Row(
            [
                dbc.Col(html.Div(
                    children = [html.P([
                    html.Label('Choose a feature'),
                    dcc.Dropdown(id = 'opt', options = opts,
                                value = opts[0], multi=False)
                        ]),
                #dropdown for districts
                html.P([
                    html.Label('Choose a district'),
                    dcc.Dropdown(id = 'opt2', options = opts2,
                                 multi=False)
                        ]),
                ]), width=4),
                dbc.Col(html.Div(dcc.Graph(id = 'plot', figure = fig_2)), width=8),
            ]),
        dbc.Row(
            [
                dbc.Col(html.Div(), width=4),
                dbc.Col(html.Div(
                    # range slider
                    html.P([
                        html.Label('Time Period'),
                        dcc.RangeSlider(id = 'slider',
                                        marks = {i: 2000+i for i in range(0,22)},
                                        min = 0,
                                        max = 21,
                                        value = [0,21])
                        ])), width=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns"), width=4),
                dbc.Col(html.Div("One of three columns"), width=4),
                dbc.Col(html.Div("One of three columns"), width=4),  
            ]),
        ]
    )
    
    # ----------------------- Callbacks and figure updates -------------------------------
    @app.callback(
        [Output('choropleth', 'figure'), 
         Output('plot', 'figure')], 
        [Input('stat', 'value'), 
         Input('opt', 'value'), 
         Input('opt2', 'value'), 
         Input('slider', 'value')])

    def update_figure(stat, input1, input2, input3):
        fig_1 = px.choropleth_mapbox(
            df_districts, geojson=geojson, color=stat,
            locations='Local Authority District Code', featureidkey= 'properties.geo_code',
            mapbox_style='dark')
        fig_1.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0},
            mapbox_zoom=4.3, # use this to zoom in on the map
            mapbox_center_lat = 54.5, # use this to align the map on latitude
            mapbox_center_lon = -3, # use this to align the map on longitude
            mapbox_accesstoken=token, # token used for getting a different map type
            width=800,
            height=750)
        
        # filtering the data
        st2 = df_dates[(df_dates['date'] > dates[input3[0]]) & (df_dates['date'] < dates[input3[1]])]
        st3 = df_districts_dates[(df_districts_dates['local_authority_district'] == input2)]

        # updating the plot
        trace_1 = go.Scatter(x = st2['date'], y = st2['nr_accidents_pd'], #trace_1 is not necessary (keeps nr_accidents_pd in plot)
                            name = 'number_accidents_pd',
                            line = dict(width = 2,
                                        color = 'rgb(10, 200, 50)'))
        trace_2 = go.Scatter(x = st2['date'], y=st2[input1],
                            name = input1,
                            line = dict(width = 2,
                                        color = 'rgb(106, 181, 135)'))
        trace_3 = go.Scatter(x=st2['date'], y=st3[input1],
                            name=input2,
                            line = dict(width = 2,
                                        color = 'rgb(300, 140, 45)')) #orange if district selected

        #return overall data fig if there is no district selected, otherwise return district fig
        if input2 is None:
            fig_2 = go.Figure(data = [trace_2], layout = layout)
        else:
            fig_2 = go.Figure(data = [trace_3], layout=layout)

        return [fig_1, fig_2]
    
    app.run_server(debug=False, dev_tools_ui=True)
