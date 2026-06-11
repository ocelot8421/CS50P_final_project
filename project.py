"""
https://dash.plotly.com/cytoscape
"""


import dash_cytoscape as cyto
from dash import Dash, html, dcc
from dash import Input, Output, State, callback
from dash_extensions import EventListener
# from elements import default_gardening_elements as gardening_steps
# from elements import user_elements as gardening_steps

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
        cyto.Cytoscape(
            id=id.CYTOSCPE,
            layout={'name': 'preset'},
            style={'width': '50%', 'height': '600px'},
            elements=elements.user_elements,
            stylesheet=stylesheet
        ),
        dcc.Markdown(id="modify_node_md"),
        html.Div(id="input_container", style={'width': '50%', 'display': 'inline'}, children=[]),
        dcc.Markdown(id="log_new_node_position"),
        dcc.Markdown(id=id.MARKDOWN_UPPER),
        dcc.Markdown(id=id.MARKDOWN_LOWER),
        dcc.Markdown(id="elements_md"),
        EventListener(
            id=id.EVENTlISTENER_TEST,
            events=[event],
            logging=True
        )
    ])
      

    # app.run(debug=True, dev_tools_hot_reload=True) # Stude NOTE dev_tools_hot_reload: https://dash.plotly.com/devtools#configuring-with-run
    app.run(debug=True)


if __name__ == '__main__':
    main()