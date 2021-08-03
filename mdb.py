from py_mongodb_model import mongodb
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()
SRV = os.getenv("SRV")
mdb = mongodb(srv_link=SRV)
mdb.config("myFirstDatabase", "fifa21")


# @st.cache(suppress_st_warning=True)
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
                            "height": "$Height",
                            "weight": "$Weight",
                            "photo": "$Photo",
                            "position": "$Position",
                            "overall": "$Overall"
                        }
                    },
                    "details": {
                        "$push": {
                            "value": "$Value",
                            "pos": {
                                "LS": "$LS",
                                "ST": "$ST",
                                "RS": "$RS",
                                "LW": "$LW",
                                "LF": "$LF",
                                "CF": "$CF",
                                "RF": "$RF",
                                "RW": "$RW",
                                "LAM": "$LAM",
                                "CAM": "$CAM",
                                "RAM": "$RAM",
                                "LM": "$LM",
                                "LCM": "$LCM",
                                "CM": "$CM",
                                "RCM": "$RCM",
                                "RM": "$RM",
                                "LWB": "$LWB",
                                "LDM": "$LDM",
                                "CDM": "$CDM",
                                "RDM": "$RDM",
                                "RWB": "$RWB",
                                "LB": "$LB",
                                "LCB": "$LCB",
                                "CB": "$CB",
                                "RCB": "$RCB",
                                "RB": "$RB",
                                "GK": "$GK",
                            },
                            "stats": {
                                "Crossing": "$Crossing",
                                "Finishing": "$Finishing",
                                "Heading Accuracy": "$Heading Accuracy",
                                "Short Passing": "$Shot Passing",
                                "Volleys": "$Volleys",
                                "Dribbling": "$Dribbling",
                                "Curve": "$Curve",
                                "FK Accuracy": "$FK Accuracy",
                                "Long Passing": "$Long Passing",
                                "Ball Control": "$Ball Control",
                                "Acceleration": "$Acceleration",
                                "Sprint Speed": "$Sprint Speed",
                                "Agility": "$Agility",
                                "Reactions": "$Reactions",
                                "Balance": "$Balance",
                                "Shot Power": "$Shot Power",
                                "Jumping": "$Jumping",
                                "Stamina": "$Stamina",
                                "Strength": "$Strength",
                                "Long Shots": "$Long Shots",
                                "Aggression": "$Aggression",
                                "Interceptions": "$Interceptions",
                                "Positioning": "$Positioning",
                                "Vision": "$Vision",
                                "Penalties": "$Penalties",
                                "Composure": "$Composure",
                                "Defensive Awareness": "$Defensive Awareness",
                                "Standing Tackle": "$Standing Tackle",
                                "Sliding Tackle": "$Sliding Tackle",
                                "GK Diving": "$GK Diving",
                                "GK Handling": "$GK Handling",
                                "GK Kicking": "$GK Kicking",
                                "GK Positioning": "$GK Positioning",
                                "GK Reflexes": "$GK Reflexes"
                            }
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
                    }
                },
                {
                    "$match": {
                        "Nationality": country,
                        "Club": club
                    }
                },
                {
                    "$group": {
                        "_id": "$Nationality",
                        "players": {
                            "$push": {
                                "name": "$Name",
                                "age": "$Age",
                                "photo": "$Photo",
                                "position": "$Position",
                                "overall": "$Overall"
                            }
                        },
                        "details": {
                            "$push": {
                                "value": "$Value",
                                "pos": {
                                    "LS": "$LS",
                                    "ST": "$ST",
                                    "RS": "$RS",
                                    "LW": "$LW",
                                    "LF": "$LF",
                                    "CF": "$CF",
                                    "RF": "$RF",
                                    "RW": "$RW",
                                    "LAM": "$LAM",
                                    "CAM": "$CAM",
                                    "RAM": "$RAM",
                                    "LM": "$LM",
                                    "LCM": "$LCM",
                                    "CM": "$CM",
                                    "RCM": "$RCM",
                                    "RM": "$RM",
                                    "LWB": "$LWB",
                                    "LDM": "$LDM",
                                    "CDM": "$CDM",
                                    "RDM": "$RDM",
                                    "RWB": "$RWB",
                                    "LB": "$LB",
                                    "LCB": "$LCB",
                                    "CB": "$CB",
                                    "RCB": "$RCB",
                                    "RB": "$RB",
                                    "GK": "$GK",
                                },
                                "stats": {
                                    "Crossing": "$Crossing",
                                    "Finishing": "$Finishing",
                                    "Heading Accuracy": "$Heading Accuracy",
                                    "Short Passing": "$Shot Passing",
                                    "Volleys": "$Volleys",
                                    "Dribbling": "$Dribbling",
                                    "Curve": "$Curve",
                                    "FK Accuracy": "$FK Accuracy",
                                    "Long Passing": "$Long Passing",
                                    "Ball Control": "$Ball Control",
                                    "Acceleration": "$Acceleration",
                                    "Sprint Speed": "$Sprint Speed",
                                    "Agility": "$Agility",
                                    "Reactions": "$Reactions",
                                    "Balance": "$Balance",
                                    "Shot Power": "$Shot Power",
                                    "Jumping": "$Jumping",
                                    "Stamina": "$Stamina",
                                    "Strength": "$Strength",
                                    "Long Shots": "$Long Shots",
                                    "Aggression": "$Aggression",
                                    "Interceptions": "$Interceptions",
                                    "Positioning": "$Positioning",
                                    "Vision": "$Vision",
                                    "Penalties": "$Penalties",
                                    "Composure": "$Composure",
                                    "Defensive Awareness": "$Defensive Awareness",
                                    "Standing Tackle": "$Standing Tackle",
                                    "Sliding Tackle": "$Sliding Tackle",
                                    "GK Diving": "$GK Diving",
                                    "GK Handling": "$GK Handling",
                                    "GK Kicking": "$GK Kicking",
                                    "GK Positioning": "$GK Positioning",
                                    "GK Reflexes": "$GK Reflexes"
                                }
                            }
                        },
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
                    "$group": {
                        "_id": "$Nationality",
                        "players": {
                            "$push": {
                                "name": "$Name",
                                "age": "$Age",
                                "photo": "$Photo",
                                "position": "$Position",
                                "overall": "$Overall"
                            }
                        },
                        "details": {
                            "$push": {
                                "value": "$Value",
                                "pos": {
                                    "LS": "$LS",
                                    "ST": "$ST",
                                    "RS": "$RS",
                                    "LW": "$LW",
                                    "LF": "$LF",
                                    "CF": "$CF",
                                    "RF": "$RF",
                                    "RW": "$RW",
                                    "LAM": "$LAM",
                                    "CAM": "$CAM",
                                    "RAM": "$RAM",
                                    "LM": "$LM",
                                    "LCM": "$LCM",
                                    "CM": "$CM",
                                    "RCM": "$RCM",
                                    "RM": "$RM",
                                    "LWB": "$LWB",
                                    "LDM": "$LDM",
                                    "CDM": "$CDM",
                                    "RDM": "$RDM",
                                    "RWB": "$RWB",
                                    "LB": "$LB",
                                    "LCB": "$LCB",
                                    "CB": "$CB",
                                    "RCB": "$RCB",
                                    "RB": "$RB",
                                    "GK": "$GK",
                                },
                                "stats": {
                                    "Crossing": "$Crossing",
                                    "Finishing": "$Finishing",
                                    "Heading Accuracy": "$Heading Accuracy",
                                    "Short Passing": "$Shot Passing",
                                    "Volleys": "$Volleys",
                                    "Dribbling": "$Dribbling",
                                    "Curve": "$Curve",
                                    "FK Accuracy": "$FK Accuracy",
                                    "Long Passing": "$Long Passing",
                                    "Ball Control": "$Ball Control",
                                    "Acceleration": "$Acceleration",
                                    "Sprint Speed": "$Sprint Speed",
                                    "Agility": "$Agility",
                                    "Reactions": "$Reactions",
                                    "Balance": "$Balance",
                                    "Shot Power": "$Shot Power",
                                    "Jumping": "$Jumping",
                                    "Stamina": "$Stamina",
                                    "Strength": "$Strength",
                                    "Long Shots": "$Long Shots",
                                    "Aggression": "$Aggression",
                                    "Interceptions": "$Interceptions",
                                    "Positioning": "$Positioning",
                                    "Vision": "$Vision",
                                    "Penalties": "$Penalties",
                                    "Composure": "$Composure",
                                    "Defensive Awareness": "$Defensive Awareness",
                                    "Standing Tackle": "$Standing Tackle",
                                    "Sliding Tackle": "$Sliding Tackle",
                                    "GK Diving": "$GK Diving",
                                    "GK Handling": "$GK Handling",
                                    "GK Kicking": "$GK Kicking",
                                    "GK Positioning": "$GK Positioning",
                                    "GK Reflexes": "$GK Reflexes"
                                }
                            }
                        },
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
                    }
                },
                {
                    "$match": {
                        "Nationality": country,
                        "Position": pos
                    }
                },
                {
                    "$group": {
                        "_id": "$Nationality",
                        "players": {
                            "$push": {
                                "name": "$Name",
                                "age": "$Age",
                                "photo": "$Photo",
                                "position": "$Position",
                                "overall": "$Overall"
                            }
                        },
                        "details": {
                            "$push": {
                                "value": "$Value",
                                "pos": {
                                    "LS": "$LS",
                                    "ST": "$ST",
                                    "RS": "$RS",
                                    "LW": "$LW",
                                    "LF": "$LF",
                                    "CF": "$CF",
                                    "RF": "$RF",
                                    "RW": "$RW",
                                    "LAM": "$LAM",
                                    "CAM": "$CAM",
                                    "RAM": "$RAM",
                                    "LM": "$LM",
                                    "LCM": "$LCM",
                                    "CM": "$CM",
                                    "RCM": "$RCM",
                                    "RM": "$RM",
                                    "LWB": "$LWB",
                                    "LDM": "$LDM",
                                    "CDM": "$CDM",
                                    "RDM": "$RDM",
                                    "RWB": "$RWB",
                                    "LB": "$LB",
                                    "LCB": "$LCB",
                                    "CB": "$CB",
                                    "RCB": "$RCB",
                                    "RB": "$RB",
                                    "GK": "$GK",
                                },
                                "stats": {
                                    "Crossing": "$Crossing",
                                    "Finishing": "$Finishing",
                                    "Heading Accuracy": "$Heading Accuracy",
                                    "Short Passing": "$Shot Passing",
                                    "Volleys": "$Volleys",
                                    "Dribbling": "$Dribbling",
                                    "Curve": "$Curve",
                                    "FK Accuracy": "$FK Accuracy",
                                    "Long Passing": "$Long Passing",
                                    "Ball Control": "$Ball Control",
                                    "Acceleration": "$Acceleration",
                                    "Sprint Speed": "$Sprint Speed",
                                    "Agility": "$Agility",
                                    "Reactions": "$Reactions",
                                    "Balance": "$Balance",
                                    "Shot Power": "$Shot Power",
                                    "Jumping": "$Jumping",
                                    "Stamina": "$Stamina",
                                    "Strength": "$Strength",
                                    "Long Shots": "$Long Shots",
                                    "Aggression": "$Aggression",
                                    "Interceptions": "$Interceptions",
                                    "Positioning": "$Positioning",
                                    "Vision": "$Vision",
                                    "Penalties": "$Penalties",
                                    "Composure": "$Composure",
                                    "Defensive Awareness": "$Defensive Awareness",
                                    "Standing Tackle": "$Standing Tackle",
                                    "Sliding Tackle": "$Sliding Tackle",
                                    "GK Diving": "$GK Diving",
                                    "GK Handling": "$GK Handling",
                                    "GK Kicking": "$GK Kicking",
                                    "GK Positioning": "$GK Positioning",
                                    "GK Reflexes": "$GK Reflexes"
                                }
                            }
                        },
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
