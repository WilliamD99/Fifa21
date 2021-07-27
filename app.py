from re import S
import streamlit as st
st.set_page_config(layout="wide")
from app import st_custom_table
from mdb import mdb_aggregate


options = st.sidebar.selectbox("Options", ["Country", "Club"])

if options == "Country":
    countries = (mdb_aggregate.get_country_all())
    country_select = st.sidebar.selectbox(
        "Select Country", countries, 0)

    if country_select:
        players = mdb_aggregate.get_players_from_country(country_select)    
        filter_club = st.sidebar.selectbox("Filter Club", players[1])
        
        if filter_club != "None":
            data = (mdb_aggregate.get_players_from_country_filter(country_select, filter_club))
            react_custom = st_custom_table(data)
        elif filter_club == "None":
            st.write(players[0])

elif options == "Club":
    clubs = mdb_aggregate.get_clubs_all()
    club_select = st.sidebar.selectbox("Clubs", clubs)

    if club_select:
        players = mdb_aggregate.get_players_from_club(club_select)
        react_custom = st_custom_table(players)