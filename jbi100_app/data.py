import plotly.express as px
import pandas as pd
import json
        
def load_accident_data(file_path : str) -> pd.DataFrame:
    df = pd.read_csv(file_path, low_memory=False)
    #dropping unnecessary columns
    df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'towing_and_articulation', 'vehicle_manoeuvre','vehicle_location_restricted_lane',
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
    # changing the date column to represent a datetime type
    df['date'] = pd.to_datetime(df['date'])
    return df

def load_population_data(file_path : str) -> pd.DataFrame:
    df = pd.read_csv(file_path, sep=';', low_memory=False)
    df['POPULATION (2018)'] = df['POPULATION (2018)'].str.replace('.','')
    return df

def load_geojson_data(file_path : str) -> dict:
    with open(file_path) as f:
        geojson = json.load(f)
        return geojson

def create_districts_df(df : pd.DataFrame) -> pd.DataFrame:
    df_grouped = df.groupby('local_authority_ons_district').sum().reset_index()
    df_grouped.drop(df_grouped.columns.difference(['local_authority_ons_district', 'accident_severity', 'number_of_vehicles','number_of_casualties']), 1, inplace=True)
    df_grouped.rename(columns = {'local_authority_ons_district':'Local Authority District Code', 'accident_severity':'Accident Severity', 'number_of_vehicles':'Number of vehicles', 'number_of_casualties':'Number of casualties'}, inplace = True)
    return df_grouped

def merge_df(df_1 : pd.DataFrame, df_2 : pd.DataFrame) -> pd.DataFrame:
    df_merge = pd.merge(df_1, df_2, left_on='Local Authority District Code', right_on='CODE', how='left', indicator=True)
    df_merge['POPULATION (2018)'].iloc[df_merge['POPULATION (2018)'] == ''] = '0'
    df_merge['POPULATION (2018)'].iloc[df_merge['_merge'] != 'both'] = '0'
    df_merge['POPULATION (2018)'] = df_merge['POPULATION (2018)'].astype(int)
    df_merge.drop(['CODE', '_merge'], axis=1, inplace=True)
    df_merge.rename(columns = {'AREA':'Local Authority District Name', 'POPULATION (2018)':'Population'}, inplace=True)
    return df_merge

def stats_per_capita(df : pd.DataFrame, stats : list) -> None:
    for stat in stats:
        name = f'{stat} Per capita'
        df[name] = df[stat] / df['Population']
        
def create_districts_dates_df(df : pd.DataFrame) -> pd.DataFrame:
    gb = df.groupby(['date', 'local_authority_district'])
    df_ret = gb.size().to_frame(name='nr_accidents_pd')
    df_ret = df_ret.join(gb.agg({'number_of_vehicles': 'sum'}).rename(columns={'number_of_vehicles':'nr_vehicles_pd'})).join(
        gb.agg({'number_of_casualties': 'sum'}).rename(columns={'number_of_casualties': 'nr_casualties_pd'})).reset_index()
    return df_ret

def create_date_df(df : pd.DataFrame) -> pd.DataFrame:
    gb = df.groupby(['date'])
    df = gb.size().to_frame(name='nr_accidents_pd')
    df = df.join(gb.agg({'number_of_vehicles': 'sum'}).rename(columns={'number_of_vehicles':'nr_vehicles_pd'})).join(
        gb.agg({'number_of_casualties': 'sum'}).rename(columns={'number_of_casualties': 'nr_casualties_pd'})).reset_index()
    return df
    
# create_districts_df, merge_df, stats_per_capita, load_accident_data, load_population_data, load_geojson_data, create_districts_dates_df, create_date_df