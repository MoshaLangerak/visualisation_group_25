#from template
from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot

from dash import html
import plotly.express as px
from dash.dependencies import Input, Output

#own imports
import pandas as pd
import data
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go


#own code

# ----------------------- Preprocessing and creating data -------------------------------

data = pd.read_csv('~/PycharmProjects/VISproject/data/all_years_2000_2020.csv', low_memory=False)


#some preprocessing here
data.drop(['Unnamed: 0', 'Unnamed: 0.1', 'towing_and_articulation', 'vehicle_manoeuvre','vehicle_location_restricted_lane',
             'junction_location', 'skidding_and_overturning', 'hit_object_in_carriageway',
             'vehicle_leaving_carriageway', 'hit_object_off_carriageway','first_point_of_impact',
             'vehicle_left_hand_drive', 'journey_purpose_of_driver', 'age_band_of_driver',
             'engine_capacity_cc', 'propulsion_code', 'age_of_vehicle',
             'driver_home_area_type', 'police_force', 'time',
             'first_road_number', 'second_road_number','did_police_officer_attend_scene_of_accident',
             'vehicle_reference', 'casualty_reference', 'age_band_of_casualty', 'pedestrian_location',
             'pedestrian_movement', 'car_passenger', 'bus_or_coach_passenger', 'casualty_home_area_type',

             'vehicle_type', 'local_authority_highway', 'urban_or_rural_area', 'lsoa_of_accident_location',
             'casualty_type', 'casualty_imd_decile'
             ], axis=1, inplace=True) #the last two rows (after the whiteline) are the columns that we're not sure of yet

#preprocessing for lineplot
data['date'] = pd.to_datetime(data['date'])

#creating a df of data per date and local authority district
gb = data.groupby(['date', 'local_authority_district'])
df_districts = gb.size().to_frame(name='nr_accidents_pd')
df_districts = df_districts.join(gb.agg({'number_of_vehicles': 'sum'}).rename(columns={'number_of_vehicles':'nr_vehicles_pd'})).join(
    gb.agg({'number_of_casualties': 'sum'}).rename(columns={'number_of_casualties': 'nr_casualties_pd'})).reset_index()
#print(df_districts[['date', 'local_authority_district','nr_accidents_pd']].head(10))

#creating a df of data per date
gb2 = data.groupby(['date'])
df = gb2.size().to_frame(name='nr_accidents_pd')
df = df.join(gb2.agg({'number_of_vehicles': 'sum'}).rename(columns={'number_of_vehicles':'nr_vehicles_pd'})).join(
    gb2.agg({'number_of_casualties': 'sum'}).rename(columns={'number_of_casualties': 'nr_casualties_pd'})).reset_index()
#print(df.head(10))


# ----------------------- Initializing options for the interactions -------------------------------

#dropdown options (for features)
available_indicators = df[['nr_accidents_pd', 'nr_vehicles_pd', 'nr_casualties_pd']] #add here all the column names/variables we want to use in the dropdown menu
opts = [{'label': 'Number of accidents', 'value': 'nr_accidents_pd'},
        {'label': 'Number of vehicles in an accident', 'value': 'nr_vehicles_pd'},
        {'label': 'Number of casualties', 'value': 'nr_casualties_pd'}]
# print(opts)
#second dropdown options (for districts)
available_indicators2 = df_districts['local_authority_district'].sort_values()
opts2 = [{'label': i, 'value': i} for i in available_indicators2.unique()]

#range slider options
dates = ['2000-01-01', '2001-01-01', '2002-01-01', '2003-01-01', '2004-01-01',
         '2005-01-01', '2006-01-01', '2007-01-01', '2008-01-01', '2009-01-01',
         '2010-01-01', '2011-01-01', '2012-01-01', '2013-01-01', '2014-01-01',
         '2015-01-01', '2016-01-01', '2017-01-01', '2018-01-01', '2019-01-01',
         '2020-01-01', '2020-12-31']
# print(dates)

# ----------------------- Initializing starting figure -------------------------------

#creating a figure
trace_1 = go.Scatter(x = df['date'], y = df['nr_accidents_pd'],
                    name = 'nr_accidents_pd',
                    line = dict(width = 2,
                                color = 'rgb(106, 181, 135)')) #green if no district selected
layout = go.Layout(title = 'Distribution of the number of accidents, vehicles and casualties over time',
                   hovermode = 'closest')
fig = go.Figure(data = [trace_1], layout = layout)

# ----------------------- Dash(board) lay-out -------------------------------

#creating a dash layout
app.layout = html.Div([
                # a header and a paragraph
                html.Div([
                    html.H1("Test dashboard Lieve"),
                    html.P("subtitle here")
                         ],
                     style = {'padding' : '50px' ,
                              'backgroundColor' : '#3aaab2'}),
                # adding a plot
                dcc.Graph(id = 'plot', figure = fig),
                # dropdown for features
                html.P([
                    html.Label("Choose a feature"),
                    dcc.Dropdown(id = 'opt', options = opts,
                                value = opts[0], multi=False)
                        ], style = {'width': '400px',
                                    'fontSize' : '20px',
                                    'padding-left' : '100px',
                                    'display': 'inline-block'}),
                #dropdown for districts
                html.P([
                    html.Label("Choose a district"),
                    dcc.Dropdown(id = 'opt2', options = opts2,
                                 multi=False)
                        ], style = {'width': '400px',
                                    'fontSize' : '20px',
                                    'padding-left' : '100px',
                                    'display': 'inline-block'}),
                # range slider
                html.P([
                    html.Label("Time Period"),
                    dcc.RangeSlider(id = 'slider',
                                    marks = {i: 2000+i for i in range(0,22)},
                                    min = 0,
                                    max = 21,
                                    value = [0,21])
                        ], style = {'width' : '80%',
                                    'fontSize' : '20px',
                                    'padding-left' : '100px',
                                    'display': 'inline-block'})
                      ])

# ----------------------- Callbacks and figure updates -------------------------------

#callback functions
@app.callback(Output('plot', 'figure'), #there is now one output (one figure) with all the dropdown/slider inputs initialized above
             [Input('opt', 'value'),
              Input('opt2', 'value'),
             Input('slider', 'value')])

def update_figure(input1, input2, input3):
    # filtering the data
    st2 = df[(df['date'] > dates[input3[0]]) & (df['date'] < dates[input3[1]])]
    st3 = df_districts[(df_districts['local_authority_district'] == input2)]
    #print(st3)
    #print(st3[input1])

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
        fig = go.Figure(data = [trace_2], layout = layout)
    else:
        fig = go.Figure(data = [trace_3], layout=layout)
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
