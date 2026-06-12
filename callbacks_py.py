from dash import Input, Output, State, callback, no_update
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
     
    print(" --------- elements:")
    for e in elements:
        print(str(e)[:140])
    print(" --------- elements vége")
    
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
        
        # with open("gardening_user.json", mode="w", encoding="utf-8") as output_file:
        #     output_file.write(json.dumps(elements, indent=4))
        with open("elements_v2.py", mode="w", encoding="utf-8") as output_file:
            output_file.write("default_gardening_elements=")
            output_file.write(str(elements))
            
                
    print(" --------- elements #2")
    for e in elements:
        print(str(e)[:140])
    print(" --------- elements vége #2")
        
    # Delete node if pressed alt+click
    # TODO


    return elements, storage


selected_by_altKey = False
## ------ INPUT callbacks ---------------------------------------------
@callback(Output('input_container', 'children'),
          Input(id.CYTOSCPE, 'tapNode'),
          State(id.EVENTlISTENER_TEST, "event"),
          prevent_initial_call=True)
def generate_input_fields(tapNode, event):
    # Flags
    global selected_by_altKey
    selected_by_altKey = not selected_by_altKey
    try:
        altKey_pressed = event['altKey']
    except:
        altKey_pressed = False
    # Labels
    filed_names = ['id', 'label', 'label_hun']

    result_fields = []
    # tap first + alt key pressed --> return input fields TODO alt+other key
    if altKey_pressed and selected_by_altKey:
        title_md = dcc.Markdown(children=["Input fields"])
        result_fields.extend([title_md])
        for name in filed_names:
            new_field = [
                    name.capitalize()+':',
                    dcc.Input(id='input_'+name, type='text', value=tapNode['data'][name])
                ]
            result_fields.extend(new_field)
    # tap second + alt key pressed --> return data list TODO only alt key
    elif altKey_pressed and not selected_by_altKey:
        title_md = dcc.Markdown(children=["Node data"])
        result_fields.extend([title_md])
        new_field = [dcc.Markdown(children=[f"* {name}: {tapNode['data'][name]}" for name in filed_names])]
        result_fields.extend(new_field)
    else:
        result_fields = []

    return result_fields

# Study NOTE: https://dash.plotly.com/dash-core-components/store#:~:text=closes.%0A%20%20%20%20dcc.Store(id%3D%7B-,%27type%27%3A%20%27storage%27%2C%20%27index%27%3A%20%27session%27,-%7D%2C%20storage_type%3D%27session%27)%2C%0A%0A%20%20%20%20html
@callback(Output(id.CYTOSCPE, 'elements', allow_duplicate=True),
          Input('input_id', 'value'),
          Input('input_label', 'value'),
          State(id.CYTOSCPE, 'elements'),
          prevent_initial_call=True)
def modify_label(id, label, elements):
    if label is None:
        return no_update
    for element in elements:
        try:
            if element['data']['label'] == label or element['data']['id'] == id:
                element['data']['label'] = label
                element['data']['id'] = id
        except:
            no_update
    return elements

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
          State(id.CYTOSCPE, 'tapNode'),
          prevent_initial_call=True)
def insert_new_node(elements, tapNode):
    result_list = []
    for element in elements:
        for key_0 in element:
            result_list.append(f"{key_0}: {element[key_0]}")
        result_list.append("\n\n")
    return "Elements:\n* " + "\n* ".join(result_list)
