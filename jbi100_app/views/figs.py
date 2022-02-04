import pandas as pd
import plotly.graph_objs as go
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from matplotlib import pyplot as plt

def get_df(dataframe, year1, year2):
    frame = dataframe.loc[(dataframe.date <= year2) & (dataframe.date >= year1)]
    return frame

def create_env_fig(fig_name, light, weather, skidding, road, site):
    figure = go.Figure()
    if fig_name == 'Light Conditions':
        figure.add_trace(go.Bar(x =get_df(light, "2000", "2004")['light_conditions'], y=get_df(light, "2000", "2005")['number_of_casualties'],
                               name = "Year 2000-2004"))
        figure.add_trace(go.Bar(x =get_df(light, "2005", "2010")['light_conditions'], y=get_df(light, "2005", "2010")['number_of_casualties'],
                               name = "Year 2005-2010"))
        figure.add_trace(go.Bar(x =get_df(light, "2011", "2015")['light_conditions'], y=get_df(light, "2011", "2015")['number_of_casualties'],
                               name = "Year 2011-2015"))
        figure.add_trace(go.Bar(x =get_df(light, "2016", "2020")['light_conditions'], y=get_df(light, "2016", "2020")['number_of_casualties'],
                               name = "Year 2016-2020"))
        
    elif fig_name == 'Weather Conditions': 
        figure.add_trace(go.Bar(x =get_df(weather, "2000", "2004")['weather_conditions'], y=get_df(weather, "2000", "2005")['number_of_casualties'],
                               name = "Year 2000-2004"))
        figure.add_trace(go.Bar(x =get_df(weather, "2005", "2010")['weather_conditions'], y=get_df(weather, "2005", "2010")['number_of_casualties'],
                               name = "Year 2005-2010"))
        figure.add_trace(go.Bar(x =get_df(weather, "2011", "2015")['weather_conditions'], y=get_df(weather, "2011", "2015")['number_of_casualties'],
                               name = "Year 2011-2015"))
        figure.add_trace(go.Bar(x =get_df(weather, "2016", "2020")['weather_conditions'], y=get_df(weather, "2016", "2020")['number_of_casualties'],
                               name = "Year 2016-2020"))
        
    elif fig_name == 'Consequence of Skidding': 
        figure.add_trace(go.Bar(x =get_df(skidding, "2000", "2004")['skidding_and_overturning'], y=get_df(skidding, "2000", "2005")['number_of_casualties'],
                               name = "Year 2000-2004"))
        figure.add_trace(go.Bar(x =get_df(skidding, "2005", "2010")['skidding_and_overturning'], y=get_df(skidding, "2005", "2010")['number_of_casualties'],
                               name = "Year 2005-2010"))
        figure.add_trace(go.Bar(x =get_df(skidding, "2011", "2015")['skidding_and_overturning'], y=get_df(skidding, "2011", "2015")['number_of_casualties'],
                               name = "Year 2011-2015"))
        figure.add_trace(go.Bar(x =get_df(skidding, "2016", "2020")['skidding_and_overturning'], y=get_df(skidding, "2016", "2020")['number_of_casualties'],
                               name = "Year 2016-2020"))
        
    
    elif fig_name == 'Surface of Road': 
        figure.add_trace(go.Bar(x =get_df(road, "2000", "2004")['road_surface_conditions'], y=get_df(road, "2000", "2005")['number_of_casualties'],
                               name = "Year 2000-2004"))
        figure.add_trace(go.Bar(x =get_df(road, "2005", "2010")['road_surface_conditions'], y=get_df(road, "2005", "2010")['number_of_casualties'],
                               name = "Year 2005-2010"))
        figure.add_trace(go.Bar(x =get_df(road, "2011", "2015")['road_surface_conditions'], y=get_df(road, "2011", "2015")['number_of_casualties'],
                               name = "Year 2011-2015"))
        figure.add_trace(go.Bar(x =get_df(road, "2016", "2020")['road_surface_conditions'], y=get_df(road, "2016", "2020")['number_of_casualties'],
                               name = "Year 2016-2020"))
        
    elif fig_name == 'Special scene at sight': 
        figure.add_trace(go.Bar(x =get_df(site, "2000", "2004")['special_conditions_at_site'], y=get_df(light, "2000", "2005")['number_of_casualties'],
                               name = "Year 2000-2004"))
        figure.add_trace(go.Bar(x =get_df(site, "2005", "2010")['special_conditions_at_site'], y=get_df(light, "2005", "2010")['number_of_casualties'],
                               name = "Year 2005-2010"))
        figure.add_trace(go.Bar(x =get_df(site, "2011", "2015")['special_conditions_at_site'], y=get_df(light, "2011", "2015")['number_of_casualties'],
                               name = "Year 2011-2015"))
        figure.add_trace(go.Bar(x =get_df(site, "2016", "2020")['special_conditions_at_site'], y=get_df(light, "2016", "2020")['number_of_casualties'],
                               name = "Year 2016-2020"))
    figure.update_layout(title_text="Various Enviormental Factors that affected number of accidents")
    
    return figure

