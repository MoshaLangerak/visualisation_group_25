import plotly.express as px
import pandas as pd


def get_data():
    # Read data
    file_path_accidants = './data/dft-road-casualty-statistics-accident-1979-2020.csv'
    file_path_casualty = './data/dft-road-casualty-statistics-casualty-1979-2020.csv'
    file_path_vehicle = './data/dft-road-casualty-statistics-vehicle-1979-2020.csv'
    
    df_accidents = pd.read_csv(file_path_accidants)
    df_casualty = pd.read_csv(file_path_casualty)
    df_vehicle = pd.read_csv(file_path_vehicle)

    # Any further data preprocessing can go her
    frames = [df_accidents, df_casualty, df_vehicle]
    df = pd.concat(frames, keys=['accidents', 'casualties', 'vehicles'])
    
    return df
