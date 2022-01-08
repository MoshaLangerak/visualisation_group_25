from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.data import create_districts_df, merge_df, stats_per_capita, load_accident_data, load_population_data, load_geojson_data

from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go


if __name__ == '__main__':
    # Create data
    file_path_1 = 'all_years_2000_2020.csv'
    file_path_2 = 'Population data 2018.csv'
    file_path_geojson = 'uk_la.geojson'

    stats = ['Accident Severity', 'Number of vehicles', 'Number of casualties']
    token = 'pk.eyJ1IjoibW9zaGEtbGFuZ2VyYWsiLCJhIjoiY2t3ZGoxMmtxMGt2ZzJudDN5NXA0YWQ4ciJ9.6QIBuYFeAajMhniiNVU-GA'
    statistics = ['Accident Severity', 'Number of vehicles', 'Number of casualties', 'Accident Severity Per capita', 'Number of vehicles Per capita', 'Number of casualties Per capita']

    df_pd = load_accident_data(file_path_1)
    df_pop = load_population_data(file_path_2)
    df_grouped = create_districts_df(df_pd)
    df_districts = merge_df(df_grouped, df_pop)
    stats_per_capita(df_districts, stats)
    geojson = load_geojson_data(file_path_geojson)

    # Instantiate custom views
    scatterplot1 = Scatterplot("Scatterplot jhgfh", 'sepal_length', 'sepal_width', df)
    scatterplot2 = Scatterplot("Scatterplot 2", 'petal_length', 'petal_width', df)
    fig = go.Figure(go.Densitymapbox(lat=df_accidents['latitude'], lon=df_accidents['longitude'], z=df_accidents['accident_severity'], radius=10))

    app.layout = html.Div(
        # dropdown
        html.P([
            html.Label("Choose a feature"),
            dcc.Dropdown(id = 'stat', 
                            options = [{'value': x, 'label': x} for x in statistics],
                            value = statistics[0])
                ], style = {'width': '400px',
                            'fontSize' : '20px',
                            'display': 'inline-block'}),
        
        dcc.Graph(id="choropleth"),
    )

    @app.callback(
        Output("choropleth", "figure"), 
        [Input("stat", "value")])

    def display_choropleth(stat):
        fig = px.choropleth_mapbox(
            df_districts, geojson=geojson, color=stat,
            locations="Local Authority District Code", featureidkey= 'properties.geo_code',
            mapbox_style='dark')
        fig.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0},
            mapbox_zoom=4.3, # use this to zoom in on the map
            mapbox_center_lat = 54.5, # use this to align the map on latitude
            mapbox_center_lon = -3, # use this to align the map on longitude
            mapbox_accesstoken=token, # token used for getting a different map type
            width=800,
            height=750)
        return fig

    
    app.run_server(debug=False, dev_tools_ui=True)
