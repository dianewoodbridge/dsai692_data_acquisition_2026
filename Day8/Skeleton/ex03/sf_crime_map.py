import streamlit as st
from load_filter_data import load_data, filter_data

crime_pd = load_data()
crime_pd = crime_pd.dropna()

st.title("SF Crime Map")


filter_column = st.selectbox('Select column to filter by:',
                             crime_pd.columns.tolist(),
                             index=None,
                             placeholder="Select a column name to filter data.",
                             accept_new_options=True)
if filter_column:
    crime_pd = filter_data(crime_pd, filter_column)

st.map(data=crime_pd, longitude="longitude",
       latitude="latitude", size=5, color="#ED5241")
