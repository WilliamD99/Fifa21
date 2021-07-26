from os import pipe

from numpy import pi
from py_mongodb_model import mongodb
import streamlit as st


SRV = "mongodb+srv://willusermongodb:UdKdQ58Cg3Yg3tK@wills.hzswp.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-98h30p-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true"

mdb = mongodb(srv_link=SRV)
mdb.config("myFirstDatabase", "fifa21")


@st.cache(suppress_st_warning=True)
class mdb_aggregate:
    def get_clubs_all():
        pipeline = [
            {
                "$project": {
                    "_id": 0,
                    "Club": 1
                }
            },
            {
                "$group": {
                    "_id": "$Club"
                }
            }
        ]
        results = list(mdb.aggregate(pipeline))
        return results

    def get_country_all():
        pipeline = [
            {
                "$project": {
                    "_id": 0,
                    "Nationality": 1
                }
            },
            {
                "$group": {
                    "_id": "$Nationality"
                }
            }
        ]
        results = list(mdb.aggregate(pipeline))

        results_lst = [data["_id"] for data in results]
        for data in results:
            results_lst.append(data["_id"])
        return results_lst

    def get_players_from_country(country):
        pipeline = [
            {
                "$project": {
                    "_id": 0,
                    "Name": 1,
                    "Age": 1,
                    "Club": 1,
                    "Club Logo": 1,
                    "Photo": 1,
                    "Position": 1,
                    "Nationality": 1
                }
            },
            {
                "$match": {
                    "Nationality": country
                }
            },
            {
                "$group": {
                    "_id": "$Club",
                    "players": {
                        "$push": {
                            "name": "$Name",
                            "age": "$Age",
                            "photo": "$Photo",
                            "position": "$Position"
                        }
                    },
                    "logo": {
                        "$first": "$Club Logo"
                    }
                }
            }
        ]
        results = list(mdb.aggregate(pipeline))

        return results
