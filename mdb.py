from dotenv import load_dotenv
import os
import streamlit as st
test = (1, 3)

from py_mongodb_model import mongodb

load_dotenv()
SRV=os.getenv("SRV")
mdb = mongodb(srv_link=SRV)
mdb.config("myFirstDatabase", "fifa21")


@st.cache(suppress_st_warning=True)
class mdb_aggregate:
    def __init__(self):
        return None

    def get_player(self, name):
        pipeline = [
            {
                "$project": {
                    "_id": 0
                }
            },
            {
                "$match": {
                    "Name": name
                }
            }
        ]
        results = list(mdb.aggregate(pipeline))
        return results

    def get_clubs_all(self):
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
            },
            {
                "$sort": {
                    "_id": 1
                }
            }
        ]
        results = list(mdb.aggregate(pipeline))
        results_lst = []
        for data in results:
            results_lst.append(data["_id"])
        return results_lst

    def get_players_from_club(self, club):
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
                    "Nationality": 1,
                    "Overall": 1
                }
            },
            {
                "$match": {
                    "Club": club
                }
            },
            {
                "$sort": {
                    "Name": 1
                }
            }
        ]
        results = list(mdb.aggregate(pipeline))

        return results

    def get_country_all(self):
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
            },
            {
                "$sort": {
                    "_id": 1
                }
            }
        ]
        results = list(mdb.aggregate(pipeline))

        results_lst = [data["_id"] for data in results]
        for data in results:
            results_lst.append(data["_id"])
        return results_lst

    def get_players_from_country(self, country):
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
                    "Nationality": 1,
                    "Overall": 1
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
                            "position": "$Position",
                            "overall": "$Overall"
                        }
                    },
                    "logo": {
                        "$first": "$Club Logo"
                    }
                }
            },
            {
                "$sort": {
                    "logo": 1
                }
            }
        ]
        results = list(mdb.aggregate(pipeline))

        club_filter = ["None"]
        for data in results:
            club_filter.append(data["_id"])

        return results, club_filter

    def get_players_from_country_filter(self, country, club, pos):
        if club == "None" and pos == "None":
            return self.get_players_from_country(country)
        elif club != "None" and pos == "None":
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
                        "Nationality": 1,
                        "Overall": 1
                    }
                },
                {
                    "$match": {
                        "Nationality": country,
                        "Club": club
                    }
                },
                {
                    "$sort": {
                        "Name": 1
                    }
                }
            ]

        elif club != "None" and pos != "None":
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
                        "Nationality": 1,
                        "Overall": 1
                    }
                },
                {
                    "$match": {
                        "Nationality": country,
                        "Club": club,
                        "Position": pos
                    }
                },
                {
                    "$sort": {
                        "Name": 1
                    }
                }
            ]
        elif club == "None" and pos != "None":
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
                        "Nationality": 1,
                        "Overall": 1
                    }
                },
                {
                    "$match": {
                        "Nationality": country,
                        "Position": pos
                    }
                },
                {
                    "$sort": {
                        "Name": 1
                    }
                }
            ]
        results = list(mdb.aggregate(pipeline))
        return results


mdb_aggregate = mdb_aggregate()
