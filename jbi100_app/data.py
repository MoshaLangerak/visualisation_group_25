import plotly.express as px
import pandas as pd
import json

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
        
def load_accident_data(file_path : str) -> pd.DataFrame:
    df = pd.read_csv(file_path, low_memory=False)
    return df

def load_population_data(file_path : str) -> pd.DataFrame:
    df = pd.read_csv(file_path, sep=';', low_memory=False)
    df['POPULATION (2018)'] = df['POPULATION (2018)'].str.replace('.','')
    return df

def load_geojson_data(file_path : str) -> dict:
    with open(file_path) as f:
        geojson = json.load(f)
        return geojson
    
# create_districts_df, merge_df, stats_per_capita, load_accident_data, load_population_data, load_geojson_data