# SiS app demonstrating visualization of polygons and geopoints

# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
import snowflake.snowpark.types as T
import snowflake.snowpark.functions as F

import numpy as np
import pandas as pd
import json
import pydeck as pdk

# Event IDs with geospatial data
# 10602642
# 10395199


st.set_page_config(
    page_title="Pydeck Polygon Layer Example App",
    page_icon="🧊",
    layout="wide")
    
# Get the current credentials
session = get_active_session()

# we will be working with this one particular event as an example
event_id_select = 10602642

# get all the data for this event
df_event = session.table('EVENTWATCH_AI.PUBLIC.EVENTWATCH_ALL_SAMPLE_V2')\
.filter(f"event_id = {event_id_select}").sort('event_publication_date')

# get the sites affected by the event
df_event_sites =df_event.select('supplier_name','site_name',
                            'site_worst_recovery_time_weeks', 'site_average_recovery_time_weeks',
                            'site_latitude','site_longitude', 'site_alternate_name') 


df_region=df_event.limit(1).select(F.col('EVENT_REGION_COORDINATES').alias('coordinates')).to_pandas()

event_row=df_event.first()


# parse the coordinates from the snowflake table with the JSON package
# and create a pandas DataFrame that Pydeck expects as data input
df_region_pandas = pd.DataFrame(data=json.loads(df_region["COORDINATES"].iloc[0]),columns=['COORDINATES'])

# this is how the polygon data looks like, it can have multiple rows
# if multiple regions are affected:
st.subheader("Polygon Data")
st.dataframe(df_region_pandas)


# create an array of polygons, in case we're dealing with multiple rows in the dataftame
my_polygons=[]

# Iterate over rows with polygons using iterrows()
for index, row in df_region_pandas.iterrows():
    coordinates_list = row["COORDINATES"]
    # Convert the list of coordinates into a numpy array
    coordinates_pairs = np.array(coordinates_list)

    # Calculate the center point so we can position the map
    center_point = np.average(coordinates_pairs, axis=0)


    polygon_layer_snow = pdk.Layer(
        "PolygonLayer",
        df_region_pandas.iloc[[index]],
        id="geojson",
        opacity=0.05,
        stroked=True,
        get_polygon="COORDINATES",
        filled=True,
        get_line_color=[200, 200, 200],
        auto_highlight=True,
        pickable=True,
    )

    my_polygons.append((polygon_layer_snow))

# create a HeatmapLayer with all the sites in the affected region
df_sites_geo =  df_event_sites.dropna().to_pandas()

sites_layer = pdk.Layer(
    'HeatmapLayer', 
    df_sites_geo,
    get_position=["SITE_LONGITUDE","SITE_LATITUDE"],
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    elevation_range=[0, 3000],
    extruded=True,
    coverage=1
)


r = pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
        latitude=center_point[1],
        longitude=center_point[0],
        zoom=3,
        pitch=50,
    ),
    layers=[my_polygons,sites_layer]    
)

st.subheader("Affected Region and Factory Sites")
st.pydeck_chart(r)

