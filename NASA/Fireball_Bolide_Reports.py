import os, csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


# Locate Data
print()
data_file = "./NASA/Fireball_And_Bolide_Reports_20240808.csv"
data = pd.read_csv(data_file)
print(data.sort_values(by='Total Radiated Energy (J)'))

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

# Coordinates to Number 
for col in ['Latitude (Deg)', 'Longitude (Deg)']:
    data[col] = data[col].apply(coord_fix)
exp = data[['Latitude (Deg)', 'Longitude (Deg)', 'Total Radiated Energy (J)', 'Calculated Total Impact Energy (kt)']].sort_values(by='Calculated Total Impact Energy (kt)', ascending=False)

data['Calculated Total Impact Energy (kt)'] = np.log(data['Calculated Total Impact Energy (kt)'])
data['Calculated Total Impact Energy (kt)'] = data['Calculated Total Impact Energy (kt)'].apply(lambda x: 0.01 if x<0.0 else x)
import os, csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


# Locate Data
print()
data_file = "./NASA/Fireball_And_Bolide_Reports_20240808.csv"
data = pd.read_csv(data_file)
print(data.sort_values(by='Total Radiated Energy (J)'))

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

# Coordinates to Number 
for col in ['Latitude (Deg)', 'Longitude (Deg)']:
    data[col] = data[col].apply(coord_fix)
exp = data[['Latitude (Deg)', 'Longitude (Deg)', 'Total Radiated Energy (J)', 'Calculated Total Impact Energy (kt)']].sort_values(by='Calculated Total Impact Energy (kt)', ascending=False)

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
figure.update_layout(mapbox_style="carto-positron")
figure.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
figure.update_layout()
figure.show()



# fig, ax = plt.subplots(figsize=(10,8))
# ax.scatter(exp['Longitude (Deg)'], exp['Latitude (Deg)'])
# plt.show()