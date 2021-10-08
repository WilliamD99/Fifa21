import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { red } from '@material-ui/core/colors';
import { Radar } from "react-chartjs-2"
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
        flexWrap: "nowrap"
    },
    media: {
        height: 0,
        paddingTop: '56.25%', // 16:9
    },
    expand: {
        transform: 'rotate(0deg)',
        marginLeft: 'auto',
        transition: theme.transitions.create('transform', {
            duration: theme.transitions.duration.shortest,
        }),
    },
    expandOpen: {
        transform: 'rotate(180deg)',
    },
    avatar: {
        backgroundColor: red[500],
    },
    control: {
        padding: theme.spacing(2),
    },
}));

export default function CellDetails(props) {
    const { details } = props
    const { stats } = details
    const classes = useStyles();
    const Attr = {
        "Atttacking": ["Crossing", "Finishing", "Heading Accuracy", "Short Passing", "Volleys"],
        "Skill": ["FK Accuracy", "Long Passing", "Ball Control", "Dribbling", "Curve"],
        "Movement": ["Acceleration", "Sprint Speed", "Agility", "Reactions", "Balance"],
        "Power": ["Shot Power", "Jumping", "Stamina", "Strength", "Long Shots"],
        "Mentality": ["Aggression", "Interceptions", "Positioning", "Vision", "Penalties", "Composure"],
        "Goal Keeping": ["GK Diving", "GK Handling", "GK Kicking", "GK Positioning", "GK Reflexes"],
        "Defending": ["Standing Tackle", "Sliding Tackle"],
    }

    const data = {
        labels: ["Pace", "Shooting", "Physical", "Passing", "Defending", "Dribbling"],
        datasets: [
            {
                label: "Basic Stats",
                data: [stats["pace"], stats["shooting"], stats["physic"], stats["passing"], stats["defending"], stats["dribbling"]],
                borderWidth: 1,
                backgroundColor: "rgba(255,99,132,0.2)",
                borderColor: "rgba(255,99,132,1)"
            }
        ]
    }
    const options = {
        scale: {
            ticks: { beginAtZero: true },
            r: {
                suggestedMin: 0,
                suggestedMax: 100
            }

        }
    }
    const attrRating = (num) => {
        let parsed = parseInt(num)
        if (parsed > 80) { 
            return "green" 
        } else if ( parsed < 50 ) { 
            return "red" 
        } else if (50 < parsed < 80) { 
            return "#E6B600"
        }
    }
    console.log(details)
    let formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'EUR',
    })
    let tagFormatter = (tags) => {
        let tagArr = tags !== undefined ? tags.split(", ") : ["None"]
        return tagArr
    }
    return (
        <>
            <Grid container>
                <h3>{details["long_name"]} ({details["player_positions"]}) ({details["club"]})</h3>
            </Grid>
            <Grid container columns={3}>
                <Grid>Value: {formatter.format(details["value"])}</Grid>
                <Grid>Wage: {formatter.format(details["wage"])}</Grid>
                <Grid>Release clause: {formatter.format(details["release_clause_eur"])}</Grid>
            </Grid>
            <Grid container columns={4} spacing={10}>
                <Grid item>
                    <h3>Profile</h3>
                    <p>Potential: {details["potential"]}</p>
                    <p>Preferred Foot: <strong>{details["preferred_foot"]}</strong></p>
                    <p>Internation Reputation: ⭐{details["international_reputation"]}</p>
                    <p>Weak Foot: ⭐{details["weak_foot"]}</p>
                    <p>Skill Moves: ⭐{details["skill_moves"]}</p>
                </Grid>
                <Grid item>
                    <h3>Specialties</h3>
                    {
                        tagFormatter(details["player_tags"]).map((e, i) => (
                            <p key={i}>{e}</p>
                        ))
                    }
                </Grid>
            </Grid>
            <Grid container style={{marginTop: "1rem", marginBottom: "1rem"}} className={classes.root} spacing={2}>
                <Grid item>
                    <Radar data={data} options={options} />
                </Grid>
                <Grid wrap="wrap" container columns={Object.keys(Attr).length} spacing={2}>
                    {
                        Object.keys(Attr).map((e, i) => (
                            <Grid item key={i}>
                                <Paper elevation={4} style={{padding: "0.5rem", width: "10rem"}}>
                                    <h3>{e}</h3>
                                    <div>
                                        {
                                            Attr[e].map((content, index) => (
                                                <div style={{marginBottom: "0.8rem"}} key={index}>
                                                    <span style={{marginRight: "1rem", border: "solid 1px", padding: "0.3rem", backgroundColor: attrRating(stats[content]), color: "white"}}>{stats[content].length > 1 ? stats[content] : `0${stats[content]}`}</span>
                                                    {content}
                                                </div>
                                            ))
                                        }
                                    </div>
                                </Paper>
                            </Grid>
                        ))
                    }
                </Grid>
            </Grid>
        </>
    )
}
