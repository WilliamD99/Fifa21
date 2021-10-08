import React, { useState } from 'react'
import TableCell from '@material-ui/core/TableCell';
import KeyboardArrowDownIcon from '@material-ui/icons/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';
import IconButton from '@material-ui/core/IconButton';
import Box from '@material-ui/core/Box';
import Collapse from '@material-ui/core/Collapse';
import TableRow from '@material-ui/core/TableRow';
import CellDetails from './CellDetails';

export default function Cell(props) {
    const { player, details } = props
    const [open, setOpen] = useState(false)
    return (
        <React.Fragment>
            <TableRow>
                <TableCell>
                    <IconButton aria-label="expand row" size="small" onClick={() => setOpen(!open)}>
                        {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                    </IconButton>
                </TableCell>
                <TableCell><img src={player["photo"]} alt="" /></TableCell>
                <TableCell>{player["name"]}</TableCell>
                <TableCell>{player["age"]}</TableCell>
                <TableCell>{player["height"]}</TableCell>
                <TableCell>{player["weight"]}</TableCell>
                <TableCell>{player["position"]}</TableCell>
                <TableCell>{player["overall"]}</TableCell>
                {/* <TableCell>{props.arr["club"]}</TableCell> */}
            </TableRow>
            <TableRow>
                <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={12}>
                    <Collapse in={open} timeout="auto" unmountOnExit>
                        <Box margin={1}>
                            <CellDetails details={details[0]}/>
                            {/* {row.history.map((historyRow) => (
                                            <TableRow key={historyRow.date}>
                                                <TableCell component="th" scope="row">
                                                    {historyRow.date}
                                                </TableCell>
                                                <TableCell>{historyRow.customerId}</TableCell>
                                                <TableCell align="right">{historyRow.amount}</TableCell>
                                                <TableCell align="right">
                                                    {Math.round(historyRow.amount * row.price * 100) / 100}
                                                </TableCell>
                                            </TableRow>
                                        ))} */}
                        </Box>
                    </Collapse>
                </TableCell>
            </TableRow>
        </React.Fragment>
    )
}
