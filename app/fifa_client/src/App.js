import React, { useEffect } from 'react'
import { withStreamlitConnection, Streamlit } from 'streamlit-component-lib'
import ST_Table from "./components/Table"
import "./styles/styles.css"

function App(props) {
  useEffect(() => Streamlit.setFrameHeight("2000"))

  return (
    <div>
      <ST_Table props={props} />
    </div>
  )
}

export default withStreamlitConnection(App)
