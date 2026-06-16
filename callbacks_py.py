from dash import html, Input, Output, State, callback, no_update, ctx
from dash import dcc
from dash_cytoscape import utils
from dash_extensions import EventListener
from dash.exceptions import PreventUpdate #Sutdy NOTE: https://dash.plotly.com/advanced-callbacks#:~:text=Input%2C%20Output%2C%20callback-,from%20dash.exceptions%20import%20PreventUpdate,-external_stylesheets%20%3D%20%5B%27https

import id
import json
import file_io
import uuid


# --------------------------------------------------------------------------------------------
# ----------------------------- CREATE NEW NODE  ---------------------------------------------
# --------------------------------------------------------------------------------------------


@callback(Output("new_node_storage", "data"),
          Input(id.EVENTlISTENER_TEST, "event"),
          Input(id.CYTOSCPE, 'tapNode'),
          State("new_node_storage", "data"),
          prevent_initial_call=True)
def calc_empty_space_clicks(event, tapNode, storage):
    # how many times should click on the empty screen to creat a new node
    trashhold = 5
    # collect keys into list
    keys_event = ['timeStamp', id.coordinate_x, id.coordinate_y]
    keys_storage = ['click_timeStamps', 'click_x_list', 'click_y_list']
    # Fill storage
    if storage is None:
        storage = {}
        storage['new_node_appendable'] = False
        storage['tapNodes'] = []
        storage['new_node_position'] = {}
        for ks in keys_storage:
            storage[ks] = []
    for i in range(len(keys_event)):
        storage[keys_storage[i]].append(event[keys_event[i]])
        # Keep last 5 clicks
        if len(storage[keys_storage[i]]) > trashhold:
            storage[keys_storage[i]] = storage[keys_storage[i]][-trashhold:]
    # Able to add new node?
    if len(storage['click_timeStamps']) == 5:
            time_difference = storage['click_timeStamps'][4]-storage['click_timeStamps'][0]
            if time_difference < 2500 and storage['click_x_list'][0] == storage['click_x_list'][4]:
                storage['new_node_appendable'] = True
            if storage['click_x_list'][0] != storage['click_x_list'][2]:
                storage['new_node_appendable'] = False
    # collect tapNodes to callibrate
    if tapNode:
        tn = {'renderedPosition': tapNode['renderedPosition'], 'relativePosition': tapNode['relativePosition']}
        if tn not in storage['tapNodes']:
            storage['tapNodes'].append(tn)
        if len(storage['tapNodes']) > 2:
            storage['tapNodes'] = storage['tapNodes'][-2:]
    # calculate relative position of new node # TODO refactor to be a bit prettier
    if storage['new_node_appendable'] and len(storage['tapNodes']) == 2:
        x0 = storage['tapNodes'][0]['relativePosition']['x']
        x0_tap = storage['tapNodes'][0]['renderedPosition']['x']
        x1 = storage['tapNodes'][1]['relativePosition']['x']
        x1_tap = storage['tapNodes'][1]['renderedPosition']['x']
        x_click = storage['click_x_list'][0]
        x = x0 + (x1-x0)*(x_click-x0_tap)/(x1_tap-x0_tap)
        y0 = storage['tapNodes'][0]['relativePosition']['y']
        y0_tap = storage['tapNodes'][0]['renderedPosition']['y']
        y1 = storage['tapNodes'][1]['relativePosition']['y']
        y1_tap = storage['tapNodes'][1]['renderedPosition']['y']
        y_click = storage['click_y_list'][0]
        y = y0 + (y1-y0)*(y_click-y0_tap)/(y1_tap-y0_tap)
        storage['new_node_position'] = {'x': x, 'y': y}
                   
    return storage


@callback(Output(id.CYTOSCPE, 'elements'),
          Output("new_node_storage", "data", allow_duplicate=True),
          State(id.CYTOSCPE, 'elements'),
          Input("new_node_storage", "data"),
          prevent_initial_call=True)
def creat_new_node(elements, storage):
    
    # Create new node
    if storage['new_node_appendable'] and storage['new_node_position'] != {}:

        # Generate id NOTE: https://docs.python.org/3/library/uuid.html
        new_id = str(uuid.uuid4())

        # Insert new node
        elements.extend([
                {
                    'data': {
                        'id': new_id,
                        'label': "new field",
                        'label_hun': 'új mező',
                    },
                    'position': storage['new_node_position'],
                    'classes': 'medium_picture'
                }])

        # Turn off "new node" mode
        storage['new_node_appendable'] = False
        
        file_io.save_elements_into_python_file(elements, "elements_v2.py")
            
    # Delete node if pressed alt+click
    # TODO

    return elements, storage



# --------------------------------------------------------------------------------------------
# ---------------------------------------- MODIFY NODE ---------------------------------------
# --------------------------------------------------------------------------------------------


node_input_fields = [
        ['data','id'],
        ['data','label'], 
        ['data','label_hun'],
        ['position','x'],
        ['position','y']
    ]
@callback(Output('node_input_container', 'children'),
          Input(id.CYTOSCPE, 'tapNode'),
          State(id.EVENTlISTENER_TEST, "event"),
          prevent_initial_call=True)
def generate_input_fields(tapNode, event):
    try:
        is_alt_tapNode = event['altKey']
    except:
        is_alt_tapNode = False
    
    # Generate input fields if Alt + TapNode pressed
    result_fields = []
    if is_alt_tapNode:        
        for name in node_input_fields:
            new_field = [
                    name[1].capitalize()+':',
                    dcc.Input(id='input_node_'+name[1], type='text', value=tapNode[name[0]][name[1]], debounce=True) # Study NOTE: https://dash.plotly.com/dash-core-components/input#debounce-delays-the-input-processing
                ]
            result_fields.extend(new_field)
        result_fields.extend([html.Button('Save', id='save_node_btn')])    
    else:
        result_fields = []

    return result_fields


# Study NOTE: https://dash.plotly.com/dash-core-components/store#:~:text=closes.%0A%20%20%20%20dcc.Store(id%3D%7B-,%27type%27%3A%20%27storage%27%2C%20%27index%27%3A%20%27session%27,-%7D%2C%20storage_type%3D%27session%27)%2C%0A%0A%20%20%20%20html
@callback(
    Output(id.CYTOSCPE, 'elements', allow_duplicate=True),
    [Input(f"input_node_{name[1]}", 'value') for name in node_input_fields],
    State(id.CYTOSCPE, 'elements'),
    prevent_initial_call=True
    )
def preshow_modified_node(id, label, label_hun, x, y, elements):
    if label is None:
        return no_update
    for element in elements:
        try:
            if element['data']['label'] == label or element['data']['id'] == id:
                
                # Collect ctx values: STUDY NOTE: https://dash.plotly.com/determining-which-callback-input-changed
                ctx_values = []
                for _,v in ctx.inputs.items():
                    ctx_values.append(v)
                for i in range(len(node_input_fields)):
                    key = node_input_fields[i]
                    element[key[0]][key[1]] = ctx_values[i]
                ctx_values = []
        except:
            no_update
    return elements


@callback(Input('save_node_btn', 'n_clicks'),
          State(id.CYTOSCPE, 'elements'))
def save_new_node_into_py_file(save_click, elements):
    if save_click is None:
        raise PreventUpdate
    else:
        file_io.save_elements_into_python_file(elements, "elements_v2.py")



# --------------------------------------------------------------------------------------------
# ---------------------------------------- DISPLAY DATA ---------------------------------------
# --------------------------------------------------------------------------------------------


@callback(Output("log_new_node_position", "children"),
          State(id.EVENTlISTENER_TEST, "event"),
          State(id.CYTOSCPE, 'tapNode'),
          Input("new_node_storage", "data"),
          prevent_initial_call=True)
def display_event(e, tapNode, storage):
    result_str = f"Event: \n* {e}"
    if storage is not None:
        result_str += f"\n\n storage: {storage}"
        if storage['new_node_appendable']:
            result_str += f"\n* Tap two node to make another new one"
    if not tapNode:
        return result_str
    # BUG: tapNode - independent from that is Input or State - shows previous state (selected or not)
    return result_str + f"\n\n TapNode: \n* renderedPosition: {tapNode['renderedPosition']} \n* timeStamp: {tapNode['timeStamp']} \n* relativePosition: {tapNode['relativePosition']}"


# Return a list of labels about selected nodes
@callback(Output(id.MARKDOWN_UPPER, 'children'),
              Input(id.CYTOSCPE, 'selectedNodeData'))
def displaySelectedNodeData(data_list):
    if data_list is None or len(data_list) == 0:
        return f"SelectedNodeData: Node has not been selected.{type(data_list)}"
    task_list = []
    for data in data_list:
        for e in data:
            task_list.append(f"{e}: {data[e][:140]}")
    return "SelectedNodeData label:\n* " + "\n* ".join(task_list) #TODO handle empty row with dot


@callback(Output(id.MARKDOWN_LOWER, 'children'),              
              Input(id.CYTOSCPE, 'tapEdgeData'),
              prevent_initial_call=True)
def display_data_in_lower_md(tapEdgeData):
    return "Tap Edge: " + str(tapEdgeData)



# --------------------------------------------------------------------------------------------
# ---------------------------------------- CREATE NEW EDGE -----------------------------------
# --------------------------------------------------------------------------------------------


is_alt_n_down = False
is_alt_n_up = False
is_alt_click = False
end_nodes_set = set()
@callback(
    Output('new_edge_storage', 'data'),
    State(id.EVENTlISTENER_TEST, "event"),
    State("keyboard", "keydown"),
    Input(id.CYTOSCPE, "tapNodeData"),
    State('new_edge_storage', 'data'),
    prevent_initial_call= True
    )
def add_edge(event, keydown, tpData, edge_storage):
    global is_alt_n_down
    global is_alt_click
    global end_nodes_set
        
    if not edge_storage: edge_storage = []
    try:
        is_alt_n_down = keydown['key'] == 'n' and keydown['altKey']
        is_alt_click = event['altKey']
    except TypeError:
        is_alt_n_down = False
        is_alt_click = False
    
    if is_alt_click and is_alt_n_down:
        try:
            if len(end_nodes_set) < 2:
                end_nodes_set.add(tpData['id'])
            elif len(end_nodes_set) == 2:
                new_id = str(uuid.uuid4())
                end_nodes_list = list(end_nodes_set)
                new_edge = {'data': {'source': f"{end_nodes_list[0]}", 'target': f"{end_nodes_list[1]}", 'id': new_id} }
                edge_storage.extend([new_edge])
                end_nodes_set = set()
        except TypeError:
            no_update
    
    # Inputs are need to update 
    is_alt_n_down = False
    is_alt_click = False
    is_alt_n_up = False
    
    return edge_storage


@callback(Output(id.CYTOSCPE, 'elements', allow_duplicate=True),
              Input('new_edge_storage', 'data'),
              State(id.CYTOSCPE, 'elements'),
              prevent_initial_call=True)
def save_new_edge_into_py_file(edge_storage, elements):
    if edge_storage:
        elements.extend(edge_storage)
        file_io.save_elements_into_python_file(elements, "elements_v2.py")
        edge_storage = []
    return elements



# --------------------------------------------------------------------------------------------
# ---------------------------------------- MODIFY EDGE ---------------------------------------
# --------------------------------------------------------------------------------------------


@callback(Output('keyboard_storage', 'data'),
    State('keyboard_storage', 'data'),
    Input("keyboard", "keydown"),
    Input("keyboard", "n_keydowns"),
    prevent_initial_call=True)
def set_True_alt_M_down(keyboard_storage, keydown, n_keydowns): 
    if not keyboard_storage:
        keyboard_storage = {}
        keyboard_storage['is_alt_M_down'] = False
    if keydown:
        keyboard_storage['is_alt_M_down'] = keydown['key'] == 'm' and keydown['altKey']
    else:
        no_update
    return keyboard_storage


@callback(Output('keyboard_storage', 'data', allow_duplicate=True),
    State('keyboard_storage', 'data'),
    Input("keyboard", "keyup"),
    Input("keyboard", "n_keyups"),
    prevent_initial_call=True)
def set_False_alt_M_down(keyboard_storage, keyup, n_keyups): 
    if not keyboard_storage:
        keyboard_storage = {}
        keyboard_storage['is_alt_M_down'] = False
    if keyup:
        if keyup['key'] == 'm':
            keyboard_storage['is_alt_M_down'] = False
        print("--keyup:", keyup['key'])
    else:
        no_update
    return keyboard_storage
          
            
@callback(Input(id.EVENTlISTENER_TEST, "event"),
          State('keyboard_storage', 'data'),
          prevent_initial_call=True)
def show_key_downs_during_clicking(click, keyboard_storage):
    if not keyboard_storage: # TODO encapsulate (3x appears at least)
        keyboard_storage = {}
        keyboard_storage['is_alt_M_down'] = False
    print("...is_alt_M_down:", keyboard_storage['is_alt_M_down'])