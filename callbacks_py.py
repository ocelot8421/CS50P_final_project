from dash import Input, Output, State, callback
from dash import dcc
from dash_cytoscape import utils
from dash_extensions import EventListener

import id
import json
import uuid


# SUTDY NOTE: https://dash.plotly.com/devtools#callback-graph


## ------ STORAGE callbacks ---------------------------------------------

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
        # print("--- x ----: ", x0, x0_tap, "  ", x1, x1_tap, "  ", x_click, "-->", x)
        y0 = storage['tapNodes'][0]['relativePosition']['y']
        y0_tap = storage['tapNodes'][0]['renderedPosition']['y']
        y1 = storage['tapNodes'][1]['relativePosition']['y']
        y1_tap = storage['tapNodes'][1]['renderedPosition']['y']
        y_click = storage['click_y_list'][0]
        y = y0 + (y1-y0)*(y_click-y0_tap)/(y1_tap-y0_tap)
        # print("--- y ----: ", y0, y0_tap, "  ", y1, y1_tap, "  ", y_click, "-->", y)
        storage['new_node_position'] = {'x': x, 'y': y}
                   
    return storage


## ------ ELEMENTS callbacks --------------------------------------------
@callback(Output(id.CYTOSCPE, 'elements'),
          Output("new_node_storage", "data", allow_duplicate=True),
          State(id.CYTOSCPE, 'elements'),
          Input("new_node_storage", "data"),
          prevent_initial_call=True)
def update_elements(elements, storage):
     
    # Create new node
    if storage['new_node_appendable'] and storage['new_node_position'] != {}:

        # Generate id NOTE: https://docs.python.org/3/library/uuid.html
        new_id = str(uuid.uuid4())

        # Insert new node
        elements.extend([
                {
                    'data': {
                        'id': new_id,
                        'label': "belabela",
                        'label_hun': 'bééélaaaa',
                    },
                    'position': storage['new_node_position'],
                    'classes': 'medium_picture'
                }])
        
        # Turn off "new node" mode
        storage['new_node_appendable'] = False
        
        with open("gardening_user.json", mode="w", encoding="utf-8") as output_file:
            output_file.write(json.dumps(elements, indent=4))
            
                
    # ..................
    
    # what is in app.layout?
    # print("app.layout:  - - - - ")
    # for e in elements:
    #     print(str(e)[:140])
    # .....................    
        
    # Delete node if pressed alt+click
    # TODO
    

    return elements, storage

@callback(Output('modify_node_md', 'children'),
          Input(id.CYTOSCPE, 'tapNode'),
          State(id.EVENTlISTENER_TEST, "event"))
def modify_node(tapNode, event):
    result_str = "Modify node:"
    try:
        altKey_pressed = event['altKey']
        result_str += "\n* alt key pressed at last nodetapping: " + str(altKey_pressed)
        if altKey_pressed:
            result_str += "\n* label: " + tapNode['data']['label']
    except TypeError:
        result_str += " ..."
    return result_str

selected_by_altKey = False
## ------ INPUT callbacks ---------------------------------------------
@callback(Output('input_container', 'children'),
          Input(id.CYTOSCPE, 'tapNode'),
          Input(id.EVENTlISTENER_TEST, "event"),
          prevent_initial_call=True)
def generate_input_fields(tapNode, event):
    # Flags
    global selected_by_altKey
    try:
        altKey_pressed = event['altKey']
    except:
        altKey_pressed = False
    # Labels
    filed_names = ['label', 'label_hun', 'something_else']
    
    result_fields = []    
    selected_by_altKey = not selected_by_altKey
    
    if altKey_pressed and selected_by_altKey:
        for name in filed_names:
            new_field = [
                    name.capitalize(),
                    dcc.Input(id='input-'+ name, type='text')
                ]
            result_fields.extend(new_field)
    elif altKey_pressed and not selected_by_altKey:
        try:
            result_fields.extend(["Place for tapNode data"])
        except:
            result_fields = []
    else:
        result_fields = []
        
    return result_fields


## ------ MARKDOWN callbacks ---------------------------------------------

@callback(Output("log_new_node_position", "children"),
          State(id.EVENTlISTENER_TEST, "event"),
          State(id.CYTOSCPE, 'tapNode'),
          Input("new_node_storage", "data"),
          prevent_initial_call=True)
def click_event(e, tapNode, storage):
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


# Return all node data
@callback(Output(id.MARKDOWN_LOWER, 'children'),
              Input(id.CYTOSCPE, 'tapNode'),
              prevent_initial_call=True)
def displaySelectedPosition(data_list):
    
    # # study NOTE: https://dash.plotly.com/cytoscape/reference#:~:text=is%20mutable%20overall).-,utils.Tree,-A%20class%20to
    # tree = utils.Tree(elements.default_gardening_elements)
    # print("TREE: ---------------")
    # print(str(tree.get_nodes())[:500])
    
    if data_list is None:
        return "TapNode has not been selected."
    result_list = [f"type: {type(data_list)}"]   
    
    for i in data_list:
        result_list.append(f"{i}: {str(data_list[i])[:140]}")
    return "TapNode:\n* " + "\n* ".join(result_list)


@callback(Output('elements_md', 'children'),
          Input(id.CYTOSCPE, 'elements'),
          Input(id.CYTOSCPE, 'tapNode'),
          prevent_initial_call=True)
def insert_new_node(elements, tapNode):
    result_list = []
    for element in elements:
        for key_0 in element:
            result_list.append(f"{key_0}: {element[key_0]}")
        result_list.append("\n\n")
    return "Elements:\n* " + "\n* ".join(result_list)
