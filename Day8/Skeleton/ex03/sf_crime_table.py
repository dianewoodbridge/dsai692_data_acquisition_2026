import streamlit as st
from load_filter_data import load_data, filter_data

crime_pd = load_data()
st.title("SF Crime")


filter_column = st.selectbox('Select column to filter by:',
                             crime_pd.columns.tolist(),
                             index=None,
                             placeholder="Select a column name to filter data.",
                             accept_new_options=True)
if filter_column:
    crime_pd = filter_data(crime_pd, filter_column)

st.dataframe(crime_pd, hide_index=True)
