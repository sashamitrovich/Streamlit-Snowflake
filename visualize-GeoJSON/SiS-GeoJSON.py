# This is a Streamlit in Snowflake app showing how to visualize GeoJSON data

# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

import streamlit as st
import pydeck as pdk
import json

session = get_active_session()

# downloaded from "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"


# get the file to local sandbox from the stage
IMG_URL = "@ml_hol_db.ml_hol_schema.geo_assets/vancouver-blocks.json"
my_file = session.file.get(IMG_URL,"file:///tmp/target")
DATA_URL = "/tmp/target/vancouver-blocks.json"

# Open the JSON file
f = open(DATA_URL) # !!! this works !!!
 
# returns JSON object as a dictionary
geojsondata = json.load(f)

# create the GeoJson layer
geojson = pdk.Layer(
    "GeoJsonLayer",
    geojsondata,
    opacity=0.8,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation="properties.valuePerSqm / 20",
    get_fill_color="[255, 255, properties.growth * 255]",
    get_line_color=[255, 255, 255],
)

LAND_COVER = [[[-123.0, 49.196], [-123.0, 49.324], [-123.306, 49.324], [-123.306, 49.196]]]

INITIAL_VIEW_STATE = pdk.ViewState(latitude=49.254, longitude=-123.13, zoom=10.5, max_zoom=16, pitch=45, bearing=0)

# create surrounding PolygonLayer
polygon = pdk.Layer(
    "PolygonLayer",
    LAND_COVER,
    stroked=False,
    # processes the data as a flat longitude-latitude pair
    get_polygon="-",
    get_fill_color=[0, 0, 0, 20],
)


# create the pydeck using the 2 layers
r = pdk.Deck(layers=[ polygon, geojson ], map_style=None, initial_view_state=INITIAL_VIEW_STATE)

# display
st.pydeck_chart(r)