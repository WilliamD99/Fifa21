from re import S
import streamlit as st
st.set_page_config(layout="wide")
from app import st_custom_table
from mdb import mdb_aggregate

pos = ["LF", "GK", "RCM", "CB", "RW", "LW", "LB", "RF", "RS", "LDM", "RAM", "RB", "CM", "ST", "LS", "LM", "CF", "RDM", "RM","CAM","LCM", "LWB", "CDM", "RWB","RCB","LCB", "LAM"]
options = st.sidebar.selectbox("Options", ["Country", "Club"])

if options == "Country":
    countries = mdb_aggregate.get_country_all()
    country_select = st.sidebar.selectbox(
        "Select Country", countries, 0)

    if country_select:
        players = mdb_aggregate.get_players_from_country(country_select)    
        filter_club = st.sidebar.selectbox("Filter Club", players[1], 0)
        filter_pos = st.sidebar.selectbox("Filter Position", ["None","ST","CF","RW","LW","CM","LM","RM","CAM","CDM","LB","RB","CB","GK","LWB","RWB"], 0)

        if filter_club:
            data = mdb_aggregate.get_players_from_country_filter(country_select, filter_club, filter_pos)
            # react_custom = st_custom_table(data)
            if type(data)=="tuple":
              st.write("helo")
            elif type(data)!= "tuple": 
              st.write(data)


elif options == "Club":
    clubs = mdb_aggregate.get_clubs_all()
    club_select = st.sidebar.selectbox("Clubs", clubs)

    if club_select:
        players = mdb_aggregate.get_players_from_club(club_select)
        react_custom = st_custom_table(players)