import streamlit.components.v1 as components

_component_func = components.declare_component(
    "custom_component",
    url="http://localhost:3000",
)


# Edit arguments sent and result received from React component, so the initial input is converted to an array and returned value extracted from the component
def st_custom_table(data: str):
    component_value = _component_func(data=data)
    return component_value
