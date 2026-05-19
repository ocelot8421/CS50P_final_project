from dash import Input, Output, State, callback
from dash_extensions import EventListener

import id






## MARKDOWN callbacks

# Return a list of labels about selected nodes
@callback(Output(id.MARKDOWN_UPPER, 'children'),
              Input(id.CYTOSCPE, 'selectedNodeData'))
def displaySelectedLabels(data_list):
    if data_list is None:
        return "No task selected."
    task_list = [str(data.get('label', 'Unknown')) for data in data_list]    
    return "You selected the following tasks:\n* " + "\n* ".join(task_list) #TODO handle empty row with dot


# Return all node data
@callback(Output(id.MARKDOWN_LOWER, 'children'),
              Input(id.CYTOSCPE, 'tapNode'))
def displaySelectedPosition(data_list):
    if data_list is None:
        return "No field selected."
    result_list = [f"{axis}: {data_list["position"][axis]}" for axis in  data_list["position"]]   
    
    for i in data_list:
        result_list.append(f"{i}: {str(data_list[i])}")
    return "Position:\n* " + "\n* ".join(result_list)

