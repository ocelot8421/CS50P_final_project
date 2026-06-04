from dash import Input, Output, State, callback
from dash_extensions import EventListener

import id



## MARKDOWN callbacks


@callback(Output("log_new_node_position", "children"),
          Input(id.EVENTlISTENER_TEST, "n_events"),
          Input(id.EVENTlISTENER_TEST, "event"),
          State(id.CYTOSCPE, 'tapNode'))
def click_event(n_events, e, tapNode):
    if not tapNode:
        return f"Event: \n* {e}"
    return f"Event: \n* {e} \n\n \
        TapNode: \n* renderedPosition: {tapNode['renderedPosition']} \n* timeStamp: {tapNode['timeStamp']} \n\n \
        Time difference: {tapNode['timeStamp'] - e['timeStamp']} \n\n \
        Postion difference x: {tapNode['renderedPosition']['x']-e['clientX']} \n\n \
        Postion difference y: {tapNode['renderedPosition']['y']-e['clientY']} \n\n "


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
              Input(id.CYTOSCPE, 'tapNode'))
def displaySelectedPosition(data_list):
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
    result_list.append(str(elements)[:200])
    return "Elements:\n* " + "\n* ".join(result_list)
