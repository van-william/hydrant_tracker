import streamlit as st
import markdown
import os
import psycopg2
import os
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from sqlalchemy import create_engine

database_path = './streamlit/hydrant_tracker.db'
engine = create_engine(f'sqlite:///{database_path}')


# Streamlit page configuration
st.set_page_config(page_title='Hydrant Tracker', layout='centered')



# Function to read data from the database
def read_data():
    query = "SELECT * FROM hydrant_status"
    return pd.read_sql(query, engine)

# Function to add data to the database
def add_data(lat, lon, status):
    query = f"INSERT INTO hydrant_status (lat, lon, status) VALUES ({lat}, {lon}, '{status}')"
    engine.execute(query)

# Streamlit app
st.title('Geospatial Data App')

# Input form
with st.form('Data Input Form'):
    lat = st.number_input('Latitude', format="%.6f")
    lon = st.number_input('Longitude', format="%.6f")
    status = st.text_input('status')
    submitted = st.form_submit_button('Submit')

    if submitted:
        add_data(lat, lon, status)

# Display map
data = read_data()
st.map(data)

import pandas as pd
from sqlalchemy import create_engine

# SQLite database URL (you can replace 'your_database.db' with your desired database name)
sqlite_url = 'sqlite:///../flask/hydrant.db'

# Create a SQLAlchemy engine
engine = create_engine(sqlite_url)

# Write the DataFrame to a SQLite table named 'your_table_name'
table_name = 'hydrant_status'
df_latlon.to_sql(table_name, engine, index=True, if_exists='replace')

# The if_exists parameter defines the behavior when the table already exists.
# 'replace' will replace the existing table, 'fail' will raise an error if the table exists,
# 'append' will add new rows to the existing table, and 'replace' will replace the existing table.

# If you want to append data to an existing table, you can use:
# df.to_sql(table_name, engine, index=False, if_exists='append')


# Create a Folium map
map_1 = folium.Map(location=[41.87, -87.6298], zoom_start=13, tiles='OpenStreetMap', attr='OSD Map')

# Add markers with tooltips
for index, row in data.iterrows():
    folium.Marker(
        [row['lat'], row['lon']],
        tooltip=row['status']
    ).add_to(map_1)

# 

# Display the map in Streamlit
st_folium(map_1, key="map")

# Alternatively, use Folium for a more interactive map
map_2 = folium.Map(location=[41.87, -87.6298], zoom_start=13, 
                   tiles='Stamen Toner',
    attr='Map data © OpenStreetMap contributors, CC-BY-SA, Tiles courtesy of Stamen Design'
)
# Add markers with tooltips
for index, row in data.iterrows():
    folium.Marker(
        [row['lat'], row['lon']],
        tooltip=row['status']
    ).add_to(map_2)
st_folium(map_2, width=700, height=500)
