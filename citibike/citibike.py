import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from snowflake.snowpark import Session
import json
from snowflake.snowpark.functions import col, call_builtin

# connect to Snowflake
with open('creds.json') as f:
    connection_parameters = json.load(f)    

session = Session.builder.configs(connection_parameters).create()
st.subheader('My Snowflake connection:')
st.write(session.sql("select current_warehouse(), current_database(), current_schema(), current_user(), current_role()").collect())

st.title('Citibike rides in NYC')


DATE_COLUMN_SNOW = 'starttime'
@st.cache
def load_snow_data(nrows):
    data = session.table("TRIPS_STATIONS_WEATHER_VW").dropna().limit(nrows) \
    .rename(col("start_lat"),"lat") \
    .rename(col("start_lon"),"lon").toPandas()

    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN_SNOW] = pd.to_datetime(data[DATE_COLUMN_SNOW])
    return data

DATE_COLUMN_SNOW = 'starttime'
def load_snow_native():
    data = session.table("TRIPS_STATIONS_WEATHER_VW") \
    .rename(col("start_lat"),"lat") \
    .rename(col("start_lon"),"lon").dropna()

    return data

# Show a slider to limit the number of records
records_to_filter = st.slider('hour', 100, 100000, 1000)  # min: 0h, max: 23h, default: 17h

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load rows of data into the dataframe.
data = load_snow_data(records_to_filter)

# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")


if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)


lowercase = lambda x: str(x).lower()

hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = load_snow_native().withColumn("hour", call_builtin("date_part", "hour", col("starttime"))) \
    .filter(col("hour")==hour_to_filter).limit(5) \
    .select(col("lat"),col("lon")) \
    .toPandas()
filtered_data.rename(lowercase, axis='columns', inplace=True)

# filtered_data = data[data[DATE_COLUMN_SNOW].dt.hour == hour_to_filter]
st.subheader(f'Map of all rides at {hour_to_filter}:00')
st.map(filtered_data)

fig, ax = plt.subplots()
sns.heatmap(filtered_data.corr(), ax=ax)
st.write(fig)

st.subheader('Number of rides by hour')

hours = load_snow_native().select(call_builtin("date_part", "hour", col("starttime")).as_("hour")) \
    .groupBy("hour").count().sort("hour").toPandas()

st.write(hours)
st.bar_chart(hours)