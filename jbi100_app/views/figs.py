import pandas as pd
import plotly.graph_objs as go
from matplotlib import pyplot as plt
import plotly.graph_objects as px

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

def create_bar_fig(purpose_accident, x_purpose_accident, detail_junction_accident, x_detail_junction_accident, control_junction_accident, x_control_junction_accident, vehicle_accident, x_vehicle_accident, manoeuvre_accident, x_manoeuvre_accident, location_junction_accident, x_location_junction_accident) -> plt.figure:
    fig_purpose_accident = px.Figure(data=[go.Bar(
    name = 'Fatal',
    x = x_purpose_accident,
    y = purpose_accident.unstack()[1].tolist()
   ),
                        go.Bar(
    name = 'Serious',
    x = x_purpose_accident,
    y = purpose_accident.unstack()[2].tolist()
                        ), 
                       go.Bar(
    name = 'Slight',
    x = x_purpose_accident,
    y = purpose_accident.unstack()[3].tolist()
                       )
                     ])


    fig_detail_junction_accident = px.Figure(data=[go.Bar(
        name = 'Fatal',
        x = x_detail_junction_accident,
        y = detail_junction_accident.unstack()[1].tolist()
    ),
                            go.Bar(
        name = 'Serious',
        x = x_detail_junction_accident,
        y = detail_junction_accident.unstack()[2].tolist()
                            ), 
                        go.Bar(
        name = 'Slight',
        x = x_detail_junction_accident,
        y = detail_junction_accident.unstack()[3].tolist()
                        )
                        ])


    fig_control_junction_accident = px.Figure(data=[go.Bar(
        name = 'Fatal',
        x = x_control_junction_accident,
        y = control_junction_accident.unstack()[1].tolist()
    ),
                            go.Bar(
        name = 'Serious',
        x = x_control_junction_accident,
        y = control_junction_accident.unstack()[2].tolist()
                            ), 
                        go.Bar(
        name = 'Slight',
        x = x_control_junction_accident,
        y = control_junction_accident.unstack()[3].tolist()
                        )
                        ])


    fig_vehicle_accident = px.Figure(data=[go.Bar(
        name = 'Fatal',
        x = x_vehicle_accident,
        y = vehicle_accident.unstack()[1].tolist()
    ),
                            go.Bar(
        name = 'Serious',
        x = x_vehicle_accident,
        y = vehicle_accident.unstack()[2].tolist()
                            ), 
                        go.Bar(
        name = 'Slight',
        x = x_vehicle_accident,
        y = vehicle_accident.unstack()[3].tolist()
                        )
                        ])


    fig_location_junction_accident = px.Figure(data=[go.Bar(
        name = 'Fatal',
        x = x_location_junction_accident,
        y = location_junction_accident.unstack()[1].tolist()
    ),
                            go.Bar(
        name = 'Serious',
        x = x_location_junction_accident,
        y = location_junction_accident.unstack()[2].tolist()
                            ), 
                        go.Bar(
        name = 'Slight',
        x = x_location_junction_accident,
        y = location_junction_accident.unstack()[3].tolist()
                        )
                        ])


    fig_manoeuvre_accident = px.Figure(data=[go.Bar(
        name = 'Fatal',
        x = x_manoeuvre_accident,
        y = manoeuvre_accident.unstack()[1].tolist()
    ),
                            go.Bar(
        name = 'Serious',
        x = x_manoeuvre_accident,
        y = manoeuvre_accident.unstack()[2].tolist()
                            ), 
                        go.Bar(
        name = 'Slight',
        x = x_manoeuvre_accident,
        y = manoeuvre_accident.unstack()[3].tolist()
                        )
                        ])


    initial = px.Figure(data=[go.Bar(
        name = 'Fatal',
        x = x_purpose_accident,
        y = purpose_accident.unstack()[1].tolist(),
        marker={'color': '#ffce30'}
    ),
                            go.Bar(
        name = 'Serious',
        x = x_purpose_accident,
        y = purpose_accident.unstack()[2].tolist(),
        marker={'color': '#5630ff'}
                            ), 
                        go.Bar(
        name = 'Slight',
        x = x_purpose_accident,
        y = purpose_accident.unstack()[3].tolist(),
        marker={'color': '#08d378'}
                        )
                        ])

    updatemenus = [
    {'buttons': [
                {
                'method': 'restyle',
                'label': 'JOURNEY PURPOSE OF DRIVER/RIDER',
                'args': [{'y': [dat.y for dat in fig_purpose_accident.data]}]
                },
                {
                'method': 'restyle',
                'label': 'JUNCTION DETAIL',
                'args': [{'y': [dat.y for dat in fig_detail_junction_accident.data]}]
                },
                {
                'method': 'restyle',
                'label': 'JUNCTION CONTROL',
                'args': [{'y': [dat.y for dat in fig_control_junction_accident.data]}]
                },
                {
                'method': 'restyle',
                'label': 'TYPE OF VEHICLE (without car)',
                'args': [{'y': [dat.y for dat in fig_vehicle_accident.data]}]
                },
                {
                'method': 'restyle',
                'label': 'JUNCTION LOCATION OF VEHICLE',
                'args': [{'y': [dat.y for dat in fig_location_junction_accident.data]}]
                },
                {
                'method': 'restyle',
                'label': 'MANOEUVRES',
                'args': [{'y': [dat.y for dat in fig_manoeuvre_accident.data]}]
                }
                ],
    'direction': 'down',
    'showactive': True,
    }
    ]

    initial = initial.update_layout(
                title_text='Features in relation with the accident severity',
                title_x=0.5,
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                legend=dict(title='Please click legend item to remove <br>or add to plot',
                            traceorder='normal',
                            bgcolor='white',
                            xanchor = 'auto'),
                plot_bgcolor= 'rgba(0, 0, 0, 0)',
                updatemenus=updatemenus
                )
    
    return initial