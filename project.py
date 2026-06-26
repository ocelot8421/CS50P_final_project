"""
project.py
"""


import dash_cytoscape as cyto
from dash import Dash, html, dcc
from dash import Input, Output, State, callback
from dash_extensions import EventListener, Keyboard
from pprint import pprint

import callbacks_py
import file_io
import elements_v2
import id
from style import stylesheet

# NOTE for study: https://docs.python.org/3/library/pprint.html#module-pprint
from pprint import pprint

    
def main():
     
    # Init application and layout
    app = Dash()
    event = {
        "event": "click",
        "props": [id.coordinate_x, id.coordinate_y, "timeStamp", "altKey"]
    }
    
    # Dinamic layout to avoid elements fall back after browser restarting
    def serve_layout():
        return html.Div([
        dcc.Store(id="new_node_storage"),
        dcc.Store(id="new_edge_storage"),
        dcc.Store(id="keyboard_storage",
                  data = {
                      'is_alt_M_down': False}),
        cyto.Cytoscape(
            id=id.CYTOSCPE,
            layout={'name': 'preset'},
            style={'height': '800px'},
            elements=file_io.load_elements(),
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
                    html.Button('Save Node', id='save_node_btn', style={'display': 'none'}),
                    html.Button('Delete Node with Edges', id='delete_node_btn', style={'display': 'none'})
                    ]
                ),
        html.Div(id="edge_input_container", style={'width': '50%', 'display': 'inline'},
                children=[
                    dcc.Input(id='input_edge_id', type='hidden'),
                    dcc.Input(id='input_edge_source', type='hidden'),                     
                    dcc.Input(id='input_edge_target', type='hidden'),
                    html.Button('Save Edge', id='save_edge_btn', style={'display': 'none'}),
                    html.Button('Flip', id='flip_edge_btn', style={'display': 'none'}),
                    html.Button('Delete Edge', id='delete_edge_btn', style={'display': 'none'})
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

    app.layout = serve_layout    
    # app.run(debug=False)
    app.run(port=8080, debug=True)
    
# --------------------- CS50P requirement - unit tests --- #1
# Serach for all task fields (nodes)

@callback(Output(id.MARKDOWN_LOWER, 'children'),              
              Input(id.CYTOSCPE, 'elements'))
def display_data_in_lower_md(elements):
    nodes = get_all_nodes(elements)
    return "Every field: " + "".join([f"\n* {node['data']['label']}" for node in nodes])


def get_all_nodes(elements):      
    nodes = []    
    for i in elements:
        if is_node(i): nodes.append(i)
    return nodes

def get_all_edges(elements):
    edges = []    
    for i in elements:
        if is_edge(i): edges.append(i)
    return edges

def get_edge_ends(elements):
    edge_ends = {
        'sources': [],
        'targets': []
    }
    for e in get_all_edges(elements):
        edge_ends['sources'].append(e['data']['source'])
        edge_ends['targets'].append(e['data']['target'])
    return edge_ends
    


def is_node(element: dict):
    if not element['data']:
        raise TypeError.add_note("Given dict is not a dash cytoscape graph element")
    return 'source' not in element['data'].keys()

def is_edge(element: dict):
    if not element['data']:
        raise TypeError.add_note("Given dict is not a dash cytoscape graph element")
    return 'source' in element['data'].keys()


# --------------------- CS50P requirement - unit tests --- #2
# Serach for all end-nodes

@callback(
    Output(id.MARKDOWN_UPPER, 'children'),
    Input(id.CYTOSCPE, 'elements')
    )
def display_in_upper_md(elements):
    nodes = get_all_leaves(elements)
    return "Every end task: " + "".join([f"\n* {node['data']['label']}" for node in nodes])

def get_all_leaves(elements):    
    leaves = []
    leaves_ids = []
    sources = get_edge_ends(elements)['sources']
    for t in get_edge_ends(elements)['targets']:
        if t not in sources:
            leaves_ids.append(t)
    for n in get_all_nodes(elements):
        if n['data']['id'] in leaves_ids:
            leaves.append(n)            
    return leaves
    

# --------------------- CS50P requirement - unit tests --- #3
# Find root


@callback(Output("log_new_node_position", "children"),
          State(id.CYTOSCPE, 'elements'),
          Input(id.CYTOSCPE, 'tapNode'),
          prevent_initial_call = True)
def find_root(elements, tapNod):
    node_id = tapNod['data']['id']
    edges = get_all_edges(elements)    
    parent_id = find_first_parent(edges, node_id)
    for node in get_all_nodes(elements):
        if node['data']['id'] == parent_id:
            return "Goal:  " + node['data']['label']
    return "No root node"
            
def find_first_parent(edges, node_id):
    for e in edges:
        if e['data']['target'] == node_id:
            parent_id = e['data']['source']
            remaining_edges = [x for x in edges if x != e]
            return find_first_parent(remaining_edges, parent_id)
    return node_id

if __name__ == '__main__':
    main()