from dash import Input, Output, State, callback
from dash_extensions import EventListener

import id


from dash_cytoscape import utils
import elements


## ------ STORAGE callbacks ---------------------------------------------

@callback(Output("new_node_storage", "data"),
          Input(id.EVENTlISTENER_TEST, "event"),
          State("new_node_storage", "data"),
          prevent_initial_call=True)
def calc_empty_space_clicks(event,storage):
    # Fill empty_clicks list    
    if storage is None:
        storage = {'empty_clicks': []}
    storage['empty_clicks'].append(event['timeStamp'])
    # Keep last 3 click
    if len(storage['empty_clicks']) > 3:
        storage['empty_clicks'] = storage['empty_clicks'][-3:]
    
    return storage

## ------ MARKDOWN callbacks ---------------------------------------------

@callback(Output("log_new_node_position", "children"),
          State(id.EVENTlISTENER_TEST, "event"),
          State(id.CYTOSCPE, 'tapNode'),
          Input("new_node_storage", "data"),
          prevent_initial_call=True)
def click_event(e, tapNode, storage):
    result_str = f"Event: \n* {e}"
    
    result_str += f"storage: {storage}"
    
    if not tapNode:
        return result_str
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
          State(id.CYTOSCPE, 'elements'),
          Input(id.CYTOSCPE, 'tapNode'),
          prevent_initial_call=True)
def insert_new_node(elements, tapNode):
    result_list = []
    for element in elements:
        for key_0 in element:
            result_list.append(f"{key_0}: {element[key_0]}")
        result_list.append("\n\n")
    return "Elements:\n* " + "\n* ".join(result_list)
