import streamlit as st


sf_crime_table_page = st.Page(
    "sf_crime_table.py", title="Table View", icon=":material/table:")
sf_crime_map_page = st.Page(
    "sf_crime_map.py", title="Map View", icon=":material/location_on:")

pg = st.navigation([sf_crime_table_page, sf_crime_map_page])
st.set_page_config(page_title="Data manager",
                   page_icon=":material/local_police:")
pg.run()
