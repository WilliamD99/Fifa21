from re import S
import streamlit as st
from app import st_custom_slider
from mdb import mdb_aggregate
import json
from bson import json_util

countries = (mdb_aggregate.get_country_all())
# Need session state because get_country_all returns values not in order each time
if "countries" not in st.session_state:
    st.session_state["countries"] = countries
country_select = st.sidebar.selectbox(
    "Select Country", st.session_state.countries, 0)

# test = json.dumps(test, default=json_util.default)
# v_custom = st_custom_slider(test, 0, 100, 50, key="slider1")
# st.write(v_custom)
if country_select:
    country_players = mdb_aggregate.get_players_from_country(country_select)
    st.write(country_players)
