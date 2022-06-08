import React, { useEffect } from 'react'
import { withStreamlitConnection, Streamlit } from 'streamlit-component-lib'
import Table from "./components/Table"
import "./styles/styles.css"
import "./styles/tailwind.css"
import "./styles/main.css"

function App(props) {
  useEffect(() => Streamlit.setFrameHeight("3000"))
  
  return (
    <div>
      <Table props={props} />
    </div>
  )
}

export default withStreamlitConnection(App)
