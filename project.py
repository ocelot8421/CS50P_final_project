"""
https://dash.plotly.com/cytoscape
"""


import dash_cytoscape as cyto
from dash import Dash, html, dcc
from dash import Input, Output, State, callback
from dash_extensions import EventListener, Keyboard
import elements_v2

import callbacks_py
import id
import elements
from style import stylesheet

# NOTE for study: https://docs.python.org/3/library/pprint.html#module-pprint
from pprint import pprint


def main():

    app = Dash()

    # NOTE for study: https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent/clientX
    event = {
        "event": "click",
        "props": [id.coordinate_x, id.coordinate_y, "timeStamp", "altKey"]
    }

    # NOTE for study: https://dash.plotly.com/dash-core-components/store
    app.layout = html.Div([
        # dcc.Store(id="new_node_storage", storage_type='session'),
        dcc.Store(id="new_node_storage"),
        dcc.Store(id="new_edge_storage"),
        dcc.Store(id="keyboard_storage",
                  data = {
                      'is_alt_M_down': False}),
        cyto.Cytoscape(
            id=id.CYTOSCPE,
            layout={'name': 'preset'},
            style={'height': '800px'},
            elements=elements_v2.default_gardening_elements,
            stylesheet=stylesheet
        ),
        dcc.Markdown(id="modify_node_md"),
        html.Div(id="node_input_container", style={'width': '50%', 'display': 'inline'},
                children=[
                    dcc.Input(id='input_node_id', type='hidden'),
                    dcc.Input(id='input_node_label', type='hidden'),                     
                    dcc.Input(id='input_node_label_hun', type='hidden'),                     
                    dcc.Input(id='input_node_x', type='hidden'),                     
                    dcc.Input(id='input_node_y', type='hidden'),                     
                    html.Button('Save', id='save_node_btn', style={'display': 'none'})
                    ]
                ),
        html.Div(id="edge_input_container", style={'width': '50%', 'display': 'inline'},
                children=[
                    dcc.Input(id='input_edge_id', type='hidden'),
                    dcc.Input(id='input_edge_source', type='hidden'),                     
                    dcc.Input(id='input_edge_target', type='hidden'),
                    html.Button('Save', id='save_edge_btn', style={'display': 'none'})
                    ]
                ),
        dcc.Markdown(id="log_new_node_position"),
        dcc.Markdown(id=id.MARKDOWN_UPPER),
        dcc.Markdown(id=id.MARKDOWN_LOWER),
        EventListener(  # Study NOTE: https://pypi.org/project/dash-extensions/0.0.67/#:~:text=your%20Dash%20app.-,EventListener,-The%20EventListener%20component
            id=id.EVENTlISTENER,
            events=[event],
            logging=True
        ),
        Keyboard(
            id="keyboard"
        )
    ])
    
    
      

    # app.run(debug=True, dev_tools_hot_reload=True) # Stude NOTE dev_tools_hot_reload: https://dash.plotly.com/devtools#configuring-with-run
    app.run(debug=True)


if __name__ == '__main__':
    main()