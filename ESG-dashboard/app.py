from matplotlib import container
import streamlit as st
import pandas as pd
import altair as alt

from snowflake.snowpark import Session, Row
from snowflake.snowpark.functions import call_udf, col
from snowflake.snowpark import functions as f

import json
# import uuid

# connect to Snowflake
with open('esg-creds.json') as fl:
    connection_parameters = json.load(fl)  
session = Session.builder.configs(connection_parameters).create()


with open('stock-creds.json') as fl:
    connection_parameters = json.load(fl)  
sessionStock = Session.builder.configs(connection_parameters).create()

st.write("# ESG Investment Analyzer :sunglasses:")


# get ESG data from the marketplace
scoreDf = session.table("TRIAL_SCO_ESG_262") # lazy evaluation

scoreWithRatingDf= scoreDf.withColumn('rating',
    f.when((f.col('"esg"') >= 0) & (f.col('"esg"') < 15),
        'CCC'
    ).when((f.col('"esg"') >= 15) & (f.col('"esg"') < 30),
        'B'
    ).when((f.col('"esg"') >= 30) & (f.col('"esg"') < 45),
        'BB'
    ).when((f.col('"esg"') >= 45) & (f.col('"esg"') < 60),
        'BBB'
    ).when((f.col('"esg"') >= 60) & (f.col('"esg"') < 75),
        'A'
    ).when((f.col('"esg"') >= 75) & (f.col('"esg"') < 90),
        'AA'
    ).when((f.col('"esg"') >= 90) & (f.col('"esg"') <= 100),
        'AAA'
    ).otherwise(
        'invalid'
    )
)

 
with open ('style.css') as fcss:
			st.markdown(f'<style>{fcss.read()}</style>', unsafe_allow_html=True)


# selectors

col1, col2 = st.columns([3,1])
with col1:
    company  = st.selectbox(
        'Choose a Company',
        scoreDf.select(col('"name"')).toPandas())

with col2:
    column  = st.selectbox(
        'Choose a Sector',
        ('Region','Sector','Industry'))

companyDf=scoreWithRatingDf.filter(col('"name"')==company) # this has the selected company row

# get the ESG values
companyScore= companyDf.select(col('"esg"')).collect()[0][0]
companyEsgE=companyDf.select(col('"esg_e"')).collect()[0][0]
companyEsgS=companyDf.select(col('"esg_s"')).collect()[0][0]
companyEsgG=companyDf.select(col('"esg_g"')).collect()[0][0]
compayEsgRating=companyDf.select(col('rating')).collect()[0][0]
companyTicker=companyDf.select(col('"ticker"')).collect()[0][0]


# TO-DO: get the data for the chart

if column=="Region":
    columnName="exch_region"
elif column=="Sector":
    columnName="economic_sector"
elif column=="Industry":
    columnName="industry"

companySelectedColumnValue = companyDf.select(col('"'+ columnName+ '"')).collect()[0][0] 

scoreWithRatingFilteredDf = scoreWithRatingDf.filter(col('"'+ columnName+ '"') == companySelectedColumnValue)

# print the chart
# df_prices.group_by(col("product_id")).sum(col("amount"))
aggDf=scoreWithRatingFilteredDf.group_by(col('rating')).agg([f.avg('"esg"').alias("Count")])
 

c = alt.Chart(aggDf.toPandas()).mark_bar().encode(
    x='RATING:O',
    y='COUNT:Q',
    color=alt.condition(
        alt.datum.RATING == compayEsgRating,  # If the condtions returns True,
        alt.value('orange'),     # which sets the bar orange.
        alt.value('steelblue')   # And if it's not true it sets the bar steelblue.
    )
)

# show the chart and the company's ESG score
col3, col4 = st.columns([3,1])
with col3:
    st.altair_chart(c, use_container_width=True)

with col4:
    st.metric(label="Company Score", value=companyScore, delta="")


# show the breakdown of company's ESG scores

col5, col6, col7 = st.columns(3)

with col5:
    st.metric(label="ESG E", value=companyEsgE, delta="")

with col6:
    st.metric(label="ESG S", value=companyEsgS, delta="")

with col7:
    st.metric(label="ESG G", value=companyEsgG, delta="")


stockDf=sessionStock.table('STOCK_HISTORY')

stockFiltered = stockDf.filter(col('symbol') == companyTicker).select(col('date'), col('close').alias('price')).sort(col('date').asc()).filter(col('date') > '2018-01-01')


c2 = alt.Chart(stockFiltered.toPandas()).mark_area(
    color="lightblue",
    interpolate='step-after',
    line=True
).encode(
    x='DATE',
    y='PRICE'
)

st.altair_chart(c2, use_container_width=True)
