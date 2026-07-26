"""
project.py
"""


import dash_cytoscape as cyto
from dash import Dash, html, dcc
from dash import Input, Output, State, callback
from dash_extensions import EventListener, Keyboard

import callbacks_py
import file_io
import id
from style import stylesheet

    
def main():
    
    # Init Dash (datavizualition framework)
    app = Dash()                                                                    #study_note_02
    
    # Define click event for eventlistener. Check the time and the alt key also.
    event = {                                                                       #study_note_01
        "event": "click",
        "props": [id.coordinate_x, id.coordinate_y, "timeStamp", "altKey"]
    }
    
    # html layout
    def serve_layout():
        
        # Dinamic layout to avoid elements fall back after browser restarting
        return html.Div([
            
        # Storages
        dcc.Store(id="new_node_storage"),
        dcc.Store(id="new_edge_storage"),
        dcc.Store(id="keyboard_storage",
                  data = {
                      'is_alt_M_down': False}),
        
        # Graph vizualiton
        cyto.Cytoscape(                                                             #study_note_02_1
            id=id.CYTOSCPE,
            layout={'name': 'preset'},
            style={'height': '800px'},
            elements=file_io.load_elements(),
            stylesheet=stylesheet
        ),
        
        # Upper markdown area
        dcc.Markdown(id="modify_node_md"),
        
        # Input containers for node and edge modification (shows up, when chosen a node or edge).
        # Node chosen via Alt + Click. Edge chosen via Alt + M + Click
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
        
        # Lower markdowns
        dcc.Markdown(id="log_new_node_position"),
        dcc.Markdown(id=id.MARKDOWN_04),
        dcc.Markdown(id=id.MARKDOWN_05),
        
        # Eventlistener. Check the time and the alt key also.
        EventListener(                                                              #study_note_01
            id=id.EVENTlISTENER,
            events=[event],
            logging=True
        ),
        
        # TODO https://dash.plotly.com/ - Eventlistenert átnyálazni 
        Keyboard(                                                                   #study_note_04
            id="keyboard"
        )
    ])

    app.layout = serve_layout                                                       #study_note_05
    app.run(port=8050, debug=True)



# --------------------------------------------------------------------------------------------
# ------------------------------ CS50P requirement -------------------------------------------
# ----------------------------------- Unit test ----------------------------------------------
# --------------------------------------- #1 -------------------------------------------------
# ----------------------- Serach for all task fields (nodes) ---------------------------------
# --------------------------------------------------------------------------------------------


@callback(Output(id.MARKDOWN_05, 'children'),              
              Input(id.CYTOSCPE, 'elements'))
def display_data_in_lower_md(elements):
    nodes = get_all_nodes(elements)
    return "Every field: " + "".join([f"\n* {node['data']['label']}" for node in nodes])

# Unit test: test_get_all_nodes()
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



# --------------------------------------------------------------------------------------------
# ------------------------------ CS50P requirement -------------------------------------------
# ----------------------------------- Unit test ----------------------------------------------
# --------------------------------------- #2 -------------------------------------------------
# --------------------- Serach for end-task fields (end-nodes) -------------------------------
# --------------------------------------------------------------------------------------------


@callback(
    Output(id.MARKDOWN_04, 'children'),
    Input(id.CYTOSCPE, 'elements')
    )
def display_in_upper_md(elements):
    nodes = get_all_leaves(elements)
    return "Every end task: " + "".join([f"\n* {node['data']['label']}" for node in nodes])

# Unit test: test_get_all_leaves()
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
    


# --------------------------------------------------------------------------------------------
# ------------------------------ CS50P requirement -------------------------------------------
# ----------------------------------- Unit test ----------------------------------------------
# --------------------------------------- #3 -------------------------------------------------
# ------------------------- Find goal fileds (root-nodes) ------------------------------------
# --------------------------------------------------------------------------------------------


# Unit test: test_find_root()
@callback(Output("log_new_node_position", "children"),
          State(id.CYTOSCPE, 'elements'),
          Input(id.CYTOSCPE, 'tapNodeData'),
          prevent_initial_call = True)
def find_root(elements, tapNodeData):
    node_id = tapNodeData['id']
    edges = get_all_edges(elements)    
    parent_id = find_first_parent(edges, node_id)
    for node in get_all_nodes(elements):
        if node['data']['id'] == parent_id:
            return "Goal > > > " + node['data']['label']
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