from py_mongodb_model import mongodb
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()
SRV = os.getenv("SRV")
mdb = mongodb(srv_link=SRV)
mdb.config("myFirstDatabase", "test")


# @st.cache(suppress_st_warning=True)
class mdb_aggregate:
    def __init__(_self):
        return None

    @st.experimental_memo
    def get_clubs_all(_self):
        pipeline = [
            {
                "$project": {
                    "_id": 0,
                    "club_name": 1
                }
            },
            {
                "$group": {
                    "_id": "$club_name"
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

    @st.experimental_memo
    def get_players_from_club(_self, club):
        pipeline = [
            {
                "$project": {
                    "_id": 0,
                }
            },
            {
                "$match": {
                    "club_name": club
                }
            },
            {
                "$group": {
                    "_id": "$club_name",
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

    @st.experimental_memo
    def get_country_all(_self):
        pipeline = [
            {
                "$project": {
                    "_id": 0,
                    "nationality": 1
                }
            },
            {
                "$group": {
                    "_id": "$nationality"
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

    @st.experimental_memo
    def get_players_from_country(_self, country):
        pipeline = [
            {
                "$project": {
                    "_id": 0,
                }
            },
            {
                "$match": {
                    "nationality": country
                }
            },
            {
                "$group": {
                    "_id": "$club_name",
                    "players": {
                        "$push": {
                            "name": "$short_name",
                            "age": "$age",
                            "height": "$height_cm",
                            "weight": "$weight_kg",
                            "photo": "$Photo",
                            "position": "$team_position",
                            "overall": "$overall"
                        }
                    },
                    "details": {
                        "$push": {
                            "value": "$value_eur",
                            "wage": "$wage_eur",
                            "release_clause_eur": "$release_clause_eur",
                            "long_name": "$long_name",
                            "dob": "$dob",
                            "player_positions": "$player_positions",
                            "potential": "$potential",
                            "preferred_foot": "$preferred_foot",
                            "player_tags": "$player_tags",
                            "club": "$club_name",
                            "international_reputation": "$international_reputation",
                            "weak_foot": "$weak_foot",
                            "skill_moves": "$skill_moves",
                            "pos": {
                                "LS": "$ls",
                                "ST": "$st",
                                "RS": "$rs",
                                "LW": "$lw",
                                "LF": "$lf",
                                "CF": "$cf",
                                "RF": "$rf",
                                "RW": "$rw",
                                "LAM": "$lam",
                                "CAM": "$cam",
                                "RAM": "$ram",
                                "LM": "$lm",
                                "LCM": "$lcm",
                                "CM": "$cm",
                                "RCM": "$rcm",
                                "RM": "$rm",
                                "LWB": "$lwb",
                                "LDM": "$ldm",
                                "CDM": "$cdm",
                                "RDM": "$rdm",
                                "RWB": "$rwb",
                                "LB": "$lb",
                                "LCB": "$lcb",
                                "CB": "$cb",
                                "RCB": "$rcb",
                                "RB": "$rb",
                                "GK": "$gk",
                                "trait": "$player_traits"
                            },
                            "stats": {
                                "pace": "$pace",
                                "shooting": "$shooting",
                                "passing": "$passing",
                                "dribbling": "$dribbling",
                                "defending": "$defending",
                                "physic": "$physic",
                                "Crossing": "$attacking_crossing",
                                "Finishing": "$attacking_finishing",
                                "Heading Accuracy": "$attacking_heading_accuracy",
                                "Short Passing": "$attacking_short_passing",
                                "Volleys": "$attacking_volleys",
                                "Dribbling": "$skill_dribbling",
                                "Curve": "$skill_curve",
                                "FK Accuracy": "$skill_fk_accuracy",
                                "Long Passing": "$skill_long_passing",
                                "Ball Control": "$skill_ball_control",
                                "Acceleration": "$movement_acceleration",
                                "Sprint Speed": "$movement_sprint_speed",
                                "Agility": "$movement_agility",
                                "Reactions": "$movement_reactions",
                                "Balance": "$movement_balance",
                                "Shot Power": "$power_shot_power",
                                "Jumping": "$power_jumping",
                                "Stamina": "$power_stamina",
                                "Strength": "$power_strength",
                                "Long Shots": "$power_long_shots",
                                "Aggression": "$mentality_aggression",
                                "Interceptions": "$mentality_interceptions",
                                "Positioning": "$mentality_positioning",
                                "Vision": "$mentality_vision",
                                "Penalties": "$mentality_penalties",
                                "Composure": "$mentality_composure",
                                "Defensive Awareness": "$Defensive Awareness",
                                "Standing Tackle": "$defending_standing_tackle",
                                "Sliding Tackle": "$defending_sliding_tackle",
                                "GK Diving": "$goalkeeping_diving",
                                "GK Handling": "$goalkeeping_handling",
                                "GK Kicking": "$goalkeeping_kicking",
                                "GK Positioning": "$goalkeeping_positioning",
                                "GK Reflexes": "$goalkeeping_reflexes"
                            }
                        }
                    },
                }
            }
        ]
        results = list(mdb.aggregate(pipeline))
        club_filter = ["None"]
        for data in results:
            club_filter.append(data["_id"])
        return results, club_filter

    @st.experimental_memo
    def get_players_from_country_filter(_self, country, club, pos):
        if club == "None" and pos == "None":
            return _self.get_players_from_country(country)
        elif club != "None" and pos == "None":
            st.write("Test")
            pipeline = [
                {
                    "$project": {
                        "_id": 0,
                    }
                },
                {
                    "$match": {
                        "nationality": country,
                        "club_name": club
                    }
                },
                {
                    "$group": {
                        "_id": "$Nationality",
                        "players": {
                            "$push": {
                                "name": "$short_name",
                                "age": "$age",
                                "photo": "$Photo",
                                "position": "$team_position",
                                "overall": "$overall",
                                "height": "$height_cm",
                                "weight": "$weight_kg"
                            }
                        },
                        "details": {
                            "$push": {
                                "value": "$value_eur",
                                "wage": "$wage_eur",
                                "release_clause_eur": "$release_clause_eur",
                                "long_name": "$long_name",
                                "dob": "$dob",
                                "player_positions": "$player_positions",
                                "potential": "$potential",
                                "preferred_foot": "$preferred_foot",
                                "player_tags": "$player_tags",
                                "club": "$club_name",
                                "international_reputation": "$international_reputation",
                                "weak_foot": "$weak_foot",
                                "skill_moves": "$skill_moves",
                                "pos": {
                                    "LS": "$ls",
                                    "ST": "$st",
                                    "RS": "$rs",
                                    "LW": "$lw",
                                    "LF": "$lf",
                                    "CF": "$cf",
                                    "RF": "$rf",
                                    "RW": "$rw",
                                    "LAM": "$lam",
                                    "CAM": "$cam",
                                    "RAM": "$ram",
                                    "LM": "$lm",
                                    "LCM": "$lcm",
                                    "CM": "$cm",
                                    "RCM": "$rcm",
                                    "RM": "$rm",
                                    "LWB": "$lwb",
                                    "LDM": "$ldm",
                                    "CDM": "$cdm",
                                    "RDM": "$rdm",
                                    "RWB": "$rwb",
                                    "LB": "$lb",
                                    "LCB": "$lcb",
                                    "CB": "$cb",
                                    "RCB": "$rcb",
                                    "RB": "$rb",
                                    "GK": "$gk",
                                    "trait": "$player_traits"
                                },
                                "stats": {
                                    "pace": "$pace",
                                    "shooting": "$shooting",
                                    "passing": "$passing",
                                    "dribbling": "$dribbling",
                                    "defending": "$defending",
                                    "physic": "$physic",
                                    "Crossing": "$attacking_crossing",
                                    "Finishing": "$attacking_finishing",
                                    "Heading Accuracy": "$attacking_heading_accuracy",
                                    "Short Passing": "$attacking_short_passing",
                                    "Volleys": "$attacking_volleys",
                                    "Dribbling": "$skill_dribbling",
                                    "Curve": "$skill_curve",
                                    "FK Accuracy": "$skill_fk_accuracy",
                                    "Long Passing": "$skill_long_passing",
                                    "Ball Control": "$skill_ball_control",
                                    "Acceleration": "$movement_acceleration",
                                    "Sprint Speed": "$movement_sprint_speed",
                                    "Agility": "$movement_agility",
                                    "Reactions": "$movement_reactions",
                                    "Balance": "$movement_balance",
                                    "Shot Power": "$power_shot_power",
                                    "Jumping": "$power_jumping",
                                    "Stamina": "$power_stamina",
                                    "Strength": "$power_strength",
                                    "Long Shots": "$power_long_shots",
                                    "Aggression": "$mentality_aggression",
                                    "Interceptions": "$mentality_interceptions",
                                    "Positioning": "$mentality_positioning",
                                    "Vision": "$mentality_vision",
                                    "Penalties": "$mentality_penalties",
                                    "Composure": "$mentality_composure",
                                    "Defensive Awareness": "$Defensive Awareness",
                                    "Standing Tackle": "$defending_standing_tackle",
                                    "Sliding Tackle": "$defending_sliding_tackle",
                                    "GK Diving": "$goalkeeping_diving",
                                    "GK Handling": "$goalkeeping_handling",
                                    "GK Kicking": "$goalkeeping_kicking",
                                    "GK Positioning": "$goalkeeping_positioning",
                                    "GK Reflexes": "$goalkeeping_reflexes"
                                }
                            }
                        }, }}
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
                        "nationality": country,
                        "club_name": club,
                        "team_position": pos
                    }
                },
                {
                    "$group": {
                        "_id": "$Nationality",
                        "players": {
                            "$push": {
                                "name": "$short_name",
                                "age": "$age",
                                "photo": "$Photo",
                                "position": "$team_position",
                                "overall": "$overall",
                                "height": "$height_cm",
                                "weight": "$weight_kg"
                            }
                        },
                        "details": {
                            "$push": {
                                "value": "$value_eur",
                                "wage": "$wage_eur",
                                "release_clause_eur": "$release_clause_eur",
                                "long_name": "$long_name",
                                "dob": "$dob",
                                "player_positions": "$player_positions",
                                "potential": "$potential",
                                "preferred_foot": "$preferred_foot",
                                "player_tags": "$player_tags",
                                "club": "$club_name",
                                "international_reputation": "$international_reputation",
                                "weak_foot": "$weak_foot",
                                "skill_moves": "$skill_moves",
                                "pos": {
                                    "LS": "$ls",
                                    "ST": "$st",
                                    "RS": "$rs",
                                    "LW": "$lw",
                                    "LF": "$lf",
                                    "CF": "$cf",
                                    "RF": "$rf",
                                    "RW": "$rw",
                                    "LAM": "$lam",
                                    "CAM": "$cam",
                                    "RAM": "$ram",
                                    "LM": "$lm",
                                    "LCM": "$lcm",
                                    "CM": "$cm",
                                    "RCM": "$rcm",
                                    "RM": "$rm",
                                    "LWB": "$lwb",
                                    "LDM": "$ldm",
                                    "CDM": "$cdm",
                                    "RDM": "$rdm",
                                    "RWB": "$rwb",
                                    "LB": "$lb",
                                    "LCB": "$lcb",
                                    "CB": "$cb",
                                    "RCB": "$rcb",
                                    "RB": "$rb",
                                    "GK": "$gk",
                                    "trait": "$player_traits"
                                },
                                "stats": {
                                    "pace": "$pace",
                                    "shooting": "$shooting",
                                    "passing": "$passing",
                                    "dribbling": "$dribbling",
                                    "defending": "$defending",
                                    "physic": "$physic",
                                    "Crossing": "$attacking_crossing",
                                    "Finishing": "$attacking_finishing",
                                    "Heading Accuracy": "$attacking_heading_accuracy",
                                    "Short Passing": "$attacking_short_passing",
                                    "Volleys": "$attacking_volleys",
                                    "Dribbling": "$skill_dribbling",
                                    "Curve": "$skill_curve",
                                    "FK Accuracy": "$skill_fk_accuracy",
                                    "Long Passing": "$skill_long_passing",
                                    "Ball Control": "$skill_ball_control",
                                    "Acceleration": "$movement_acceleration",
                                    "Sprint Speed": "$movement_sprint_speed",
                                    "Agility": "$movement_agility",
                                    "Reactions": "$movement_reactions",
                                    "Balance": "$movement_balance",
                                    "Shot Power": "$power_shot_power",
                                    "Jumping": "$power_jumping",
                                    "Stamina": "$power_stamina",
                                    "Strength": "$power_strength",
                                    "Long Shots": "$power_long_shots",
                                    "Aggression": "$mentality_aggression",
                                    "Interceptions": "$mentality_interceptions",
                                    "Positioning": "$mentality_positioning",
                                    "Vision": "$mentality_vision",
                                    "Penalties": "$mentality_penalties",
                                    "Composure": "$mentality_composure",
                                    "Defensive Awareness": "$Defensive Awareness",
                                    "Standing Tackle": "$defending_standing_tackle",
                                    "Sliding Tackle": "$defending_sliding_tackle",
                                    "GK Diving": "$goalkeeping_diving",
                                    "GK Handling": "$goalkeeping_handling",
                                    "GK Kicking": "$goalkeeping_kicking",
                                    "GK Positioning": "$goalkeeping_positioning",
                                    "GK Reflexes": "$goalkeeping_reflexes"
                                }
                            }
                        }, }}
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
                        "nationality": country,
                        "team_position": pos
                    }
                },
                {
                    "$group": {
                        "_id": "$Nationality",
                        "players": {
                            "$push": {
                                "name": "$short_name",
                                "age": "$age",
                                "photo": "$Photo",
                                "position": "$team_position",
                                "overall": "$overall",
                                "height": "$height_cm",
                                "weight": "$weight_kg"
                            }
                        },
                        "details": {
                            "$push": {
                                "value": "$value_eur",
                                "wage": "$wage_eur",
                                "release_clause_eur": "$release_clause_eur",
                                "long_name": "$long_name",
                                "dob": "$dob",
                                "player_positions": "$player_positions",
                                "potential": "$potential",
                                "preferred_foot": "$preferred_foot",
                                "player_tags": "$player_tags",
                                "club": "$club_name",
                                "international_reputation": "$international_reputation",
                                "weak_foot": "$weak_foot",
                                "skill_moves": "$skill_moves",
                                "pos": {
                                    "LS": "$ls",
                                    "ST": "$st",
                                    "RS": "$rs",
                                    "LW": "$lw",
                                    "LF": "$lf",
                                    "CF": "$cf",
                                    "RF": "$rf",
                                    "RW": "$rw",
                                    "LAM": "$lam",
                                    "CAM": "$cam",
                                    "RAM": "$ram",
                                    "LM": "$lm",
                                    "LCM": "$lcm",
                                    "CM": "$cm",
                                    "RCM": "$rcm",
                                    "RM": "$rm",
                                    "LWB": "$lwb",
                                    "LDM": "$ldm",
                                    "CDM": "$cdm",
                                    "RDM": "$rdm",
                                    "RWB": "$rwb",
                                    "LB": "$lb",
                                    "LCB": "$lcb",
                                    "CB": "$cb",
                                    "RCB": "$rcb",
                                    "RB": "$rb",
                                    "GK": "$gk",
                                    "trait": "$player_traits"
                                },
                                "stats": {
                                    "pace": "$pace",
                                    "shooting": "$shooting",
                                    "passing": "$passing",
                                    "dribbling": "$dribbling",
                                    "defending": "$defending",
                                    "physic": "$physic",
                                    "Crossing": "$attacking_crossing",
                                    "Finishing": "$attacking_finishing",
                                    "Heading Accuracy": "$attacking_heading_accuracy",
                                    "Short Passing": "$attacking_short_passing",
                                    "Volleys": "$attacking_volleys",
                                    "Dribbling": "$skill_dribbling",
                                    "Curve": "$skill_curve",
                                    "FK Accuracy": "$skill_fk_accuracy",
                                    "Long Passing": "$skill_long_passing",
                                    "Ball Control": "$skill_ball_control",
                                    "Acceleration": "$movement_acceleration",
                                    "Sprint Speed": "$movement_sprint_speed",
                                    "Agility": "$movement_agility",
                                    "Reactions": "$movement_reactions",
                                    "Balance": "$movement_balance",
                                    "Shot Power": "$power_shot_power",
                                    "Jumping": "$power_jumping",
                                    "Stamina": "$power_stamina",
                                    "Strength": "$power_strength",
                                    "Long Shots": "$power_long_shots",
                                    "Aggression": "$mentality_aggression",
                                    "Interceptions": "$mentality_interceptions",
                                    "Positioning": "$mentality_positioning",
                                    "Vision": "$mentality_vision",
                                    "Penalties": "$mentality_penalties",
                                    "Composure": "$mentality_composure",
                                    "Defensive Awareness": "$Defensive Awareness",
                                    "Standing Tackle": "$defending_standing_tackle",
                                    "Sliding Tackle": "$defending_sliding_tackle",
                                    "GK Diving": "$goalkeeping_diving",
                                    "GK Handling": "$goalkeeping_handling",
                                    "GK Kicking": "$goalkeeping_kicking",
                                    "GK Positioning": "$goalkeeping_positioning",
                                    "GK Reflexes": "$goalkeeping_reflexes"
                                }
                            }
                        }, }}
            ]
        results = list(mdb.aggregate(pipeline))
        return results

    @st.experimental_memo
    def get_player_from_search(_self, query):
        pipeline = [
            {
                "$project": {
                    "_id": 0
                }
            },
            {
                "$match": {
                    "short_name": {
                        "$regex": query
                    }
                }
            },
            {
                "$group": {
                    "_id": "$club_name",
                    "players": {
                        "$push": {
                            "name": "$short_name",
                            "age": "$age",
                            "height": "$height_cm",
                            "weight": "$weight_kg",
                            "photo": "$Photo",
                            "position": "$team_position",
                            "overall": "$overall"
                        }
                    },
                    "details": {
                        "$push": {
                            "value": "$value_eur",
                            "wage": "$wage_eur",
                            "release_clause_eur": "$release_clause_eur",
                            "long_name": "$long_name",
                            "dob": "$dob",
                            "player_positions": "$player_positions",
                            "potential": "$potential",
                            "preferred_foot": "$preferred_foot",
                            "player_tags": "$player_tags",
                            "club": "$club_name",
                            "international_reputation": "$international_reputation",
                            "weak_foot": "$weak_foot",
                            "skill_moves": "$skill_moves",
                            "pos": {
                                "LS": "$ls",
                                "ST": "$st",
                                "RS": "$rs",
                                "LW": "$lw",
                                "LF": "$lf",
                                "CF": "$cf",
                                "RF": "$rf",
                                "RW": "$rw",
                                "LAM": "$lam",
                                "CAM": "$cam",
                                "RAM": "$ram",
                                "LM": "$lm",
                                "LCM": "$lcm",
                                "CM": "$cm",
                                "RCM": "$rcm",
                                "RM": "$rm",
                                "LWB": "$lwb",
                                "LDM": "$ldm",
                                "CDM": "$cdm",
                                "RDM": "$rdm",
                                "RWB": "$rwb",
                                "LB": "$lb",
                                "LCB": "$lcb",
                                "CB": "$cb",
                                "RCB": "$rcb",
                                "RB": "$rb",
                                "GK": "$gk",
                                "trait": "$player_traits"
                            },
                            "stats": {
                                "pace": "$pace",
                                "shooting": "$shooting",
                                "passing": "$passing",
                                "dribbling": "$dribbling",
                                "defending": "$defending",
                                "physic": "$physic",
                                "Crossing": "$attacking_crossing",
                                "Finishing": "$attacking_finishing",
                                "Heading Accuracy": "$attacking_heading_accuracy",
                                "Short Passing": "$attacking_short_passing",
                                "Volleys": "$attacking_volleys",
                                "Dribbling": "$skill_dribbling",
                                "Curve": "$skill_curve",
                                "FK Accuracy": "$skill_fk_accuracy",
                                "Long Passing": "$skill_long_passing",
                                "Ball Control": "$skill_ball_control",
                                "Acceleration": "$movement_acceleration",
                                "Sprint Speed": "$movement_sprint_speed",
                                "Agility": "$movement_agility",
                                "Reactions": "$movement_reactions",
                                "Balance": "$movement_balance",
                                "Shot Power": "$power_shot_power",
                                "Jumping": "$power_jumping",
                                "Stamina": "$power_stamina",
                                "Strength": "$power_strength",
                                "Long Shots": "$power_long_shots",
                                "Aggression": "$mentality_aggression",
                                "Interceptions": "$mentality_interceptions",
                                "Positioning": "$mentality_positioning",
                                "Vision": "$mentality_vision",
                                "Penalties": "$mentality_penalties",
                                "Composure": "$mentality_composure",
                                "Defensive Awareness": "$Defensive Awareness",
                                "Standing Tackle": "$defending_standing_tackle",
                                "Sliding Tackle": "$defending_sliding_tackle",
                                "GK Diving": "$goalkeeping_diving",
                                "GK Handling": "$goalkeeping_handling",
                                "GK Kicking": "$goalkeeping_kicking",
                                "GK Positioning": "$goalkeeping_positioning",
                                "GK Reflexes": "$goalkeeping_reflexes"
                            }
                        }
                    },
                }}
        ]
        results = list(mdb.aggregate(pipeline))
        return results


mdb_aggregate = mdb_aggregate()
