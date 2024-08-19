import os, csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm #colormap
import plotly.express as px
import plotly.graph_objects as go

##################################################################
# Data downloaded from NASA Open Source Datasets:
# URL: https://data.nasa.gov/Space-Science/Fireball-And-Bolide-Reports/mc52-syum/about_data
# DL-Date: Friday August 9th, 2024
# Author (code): Peter Clark / git: peter-clark
##################################################################

## Functions for plotting and program orderedness 
def coord_fix(coordinate):
    # coordinate[:-1] is DIRECTION Letter.
    # compare against W or N, if not, flip sign to neg
    if not coordinate or len(coordinate) < 2:
        return None  # Or some default value like 0 or np.nan
    
    # Extract the numeric part and apply the direction adjustment
    try:
        return float(coordinate[:-1]) * (-1 if coordinate[-1] in ['W', 'S'] else 1)
    except ValueError:
        return None  # Handle cases where conversion fails

def get_color(value):
    norm = mcolors.Normalize(vmin=0, vmax=1)
    cmap = cm.get_cmap('RdYlGn_r')  # Reversed to go from green to red
    rgb = cmap(norm(value))[:3]  # Get the RGB tuple, ignore the alpha channel
    return f'rgb({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)})'

def map_plot(data):
    data['log Calculated Total Impact Energy (kt)'] = np.log(data['Calculated Total Impact Energy (kt)'])
    data['log Calculated Total Impact Energy (kt)'] = data['log Calculated Total Impact Energy (kt)'].apply(lambda x: 0.5 if x<0.0 else x)

    color_scale = [(0, 'green'),(1,'red')]
    figure = px.scatter_mapbox(data,
                            lat='Latitude (Deg)',
                            lon='Longitude (Deg)',
                            size='log Calculated Total Impact Energy (kt)',
                            color='log Calculated Total Impact Energy (kt)',
                            color_continuous_scale=color_scale,
                            hover_data=['Latitude (Deg)', 'Longitude (Deg)',
                                        'Calculated Total Impact Energy (kt)',
                                        'Date/Time - Peak Brightness (UT)'],
                            height=800,
                            width=1600,
                            zoom=1,
    )

    # Add vectors to the map
    data['Norm Velocity Components (km/s): vz']=np.abs(data['Velocity Components (km/s): vz']/100)
    data['Norm Velocity Components (km/s): vz'] = data['Norm Velocity Components (km/s): vz'].fillna(0.01)
    for _, row in data.iterrows():
        val = row['Norm Velocity Components (km/s): vz']
        w = val*10
        vcolor = get_color(row["log Calculated Total Impact Energy (kt)"])
        figure.add_trace(go.Scattermapbox(
            lon=[row['Longitude (Deg)'], row['Longitude (Deg)'] + -1*row['Velocity Components (km/s): vx']],
            lat=[row['Latitude (Deg)'], row['Latitude (Deg)'] + -1*row['Velocity Components (km/s): vy']],
            mode='lines',
            line=dict(width=w, color=vcolor),
            name='Vector'
        ))

    # Update layout for better visualization
    figure.update_layout(
        mapbox=dict(
            center=dict(lat=40, lon=-95),
            zoom=1,
        ),
        showlegend=False,
    )
    figure.update_layout(mapbox_style="carto-positron")
    figure.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    figure.update_layout()
    figure.show()

def velocity_plot(data):
    ax = px.scatter_3d(data, x='Velocity Components (km/s): vx', y='Velocity Components (km/s): vy', 
                    z='Velocity Components (km/s): vz', color='log Calculated Total Impact Energy (kt)')
    x_range = data['Velocity Components (km/s): vx'].min(), data['Velocity Components (km/s): vx'].max()
    y_range = data['Velocity Components (km/s): vy'].min(), data['Velocity Components (km/s): vy'].max()
    z_range = data['Velocity Components (km/s): vz'].min(), data['Velocity Components (km/s): vz'].max()
    ax.add_trace(go.Scatter3d(x=x_range, y=[0,0], z=[0,0], mode='lines', line=dict(color='red', width=2)))
    ax.add_trace(go.Scatter3d(x=[0,0], y=y_range, z=[0,0], mode='lines', line=dict(color='green', width=2)))
    ax.add_trace(go.Scatter3d(x=[0,0], y=[0,0], z=z_range, mode='lines', line=dict(color='blue', width=2)))
    ax.show()



if __name__ == '__main__':

    # Locate Data
    data_file = "./NASA/Fireball_And_Bolide_Reports_20240808.csv"
    data = pd.read_csv(data_file)
    #print(data.sort_values(by='Total Radiated Energy (J)'))

    # Coordinates to Number 
    for col in ['Latitude (Deg)', 'Longitude (Deg)']:
        data[col] = data[col].apply(coord_fix)
    exp = data[['Latitude (Deg)', 'Longitude (Deg)', 'Total Radiated Energy (J)', 'Calculated Total Impact Energy (kt)']].sort_values(by='Calculated Total Impact Energy (kt)', ascending=False)
    
    map_plot(data)
    velocity_plot(data)

    # Angular velocity? vs total energy?
    # Randomness check w correlations (even distributions of factors: location, power, etc.)