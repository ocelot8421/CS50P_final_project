#study_note_01
```EventListener()```
https://pypi.org/project/dash-extensions/0.0.68/#:~:text=example%20app%20above.-,EventListener,-The%20EventListener%20component

#study_note_02
```Dash()```
https://dash.plotly.com/cytoscape#:~:text=dash_cytoscape%20as%20cyto-,app%20%3D%20Dash(),-app.layout%20%3D%20html

#study_note_02_1
```cyto.Cytoscape(```
https://dash.plotly.com/cytoscape#:~:text=layout%20%3D%20html.Div(%5B-,cyto.Cytoscape(,-id%3D%27cytoscape

#study_note_03
```import json```
https://cs50.harvard.edu/python/notes/4/#:~:text=received.%20Modify%20your%20code%20as%20follows%3A-,import%20json,-import%20requests%0Aimport%20sys%0A%0Aif%20len

#study_note_04
```Input("keyboard", "n_keydowns")```
https://github.com/emilhe/dash-extensions/issues/11#:~:text=%5BInput(%22keyboard%22%2C%20%22n_keydowns%22)%5D%2C

#study_note_05
```app.layout = serve_layout```
https://cs50.harvard.edu/python/notes/6/#:~:text=%2C%20key%3D-,get_name,-)%3A%0A%20%20%20%20print(


"TREE: ---------------"
study NOTE: https://dash.plotly.com/cytoscape/reference#:~:text=is%20mutable%20overall).-,utils.Tree,-A%20class%20to
    tree = utils.Tree(elements.default_gardening_elements)
    print(str(tree.get_nodes())[:500])

SUTDY NOTE: https://dash.plotly.com/devtools#callback-graph


# os.mkdirs
https://www.w3schools.com/python/ref_os_makedirs.asp


https://www.geeksforgeeks.org/python/python-os-path-exists-method/

# platformdirs - user data and directories handling
https://platformdirs.readthedocs.io/en/latest/tutorial.html#finding-your-first-directory

# @decorator
https://medium.com/@2019077_13406/deciphering-decorators-in-python-a50eb99a29c9
```
def simple_decorator(func):
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

@simple_decorator
def say_hello():
    print("Hello!")

def say_hello_without_decorator():
    print("Hello!")

say_hello()
say_hello_func = simple_decorator(say_hello_without_decorator)
print("")
say_hello_func()
```

# Input delays
```
dcc.Input(id='input_edge_'+name, type='text', value=tapEdgeData[name], debounce=True)
```
Study NOTE: https://dash.plotly.com/dash-core-components/input#debounce-delays-the-input-processing

# PreventUpdate
https://dash.plotly.com/advanced-callbacks#:~:text=Input%2C%20Output%2C%20callback-,from%20dash.exceptions%20import%20PreventUpdate,-external_stylesheets%20%3D%20%5B%27https

# Dash Cytoscape
https://dash.plotly.com/cytoscape

# MouseEvent/clientX 
https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent/clientX
```
event = {
    "event": "click",
    "props": [id.coordinate_x, id.coordinate_y, "timeStamp", "altKey"]
}
```

# Storage - store data between callbacks
https://dash.plotly.com/dash-core-components/store
```
app.layout = html.Div([
    # dcc.Store(id="new_node_storage", storage_type='session'),
    dcc.Store(id="new_node_storage"),
    dcc.Store(id="new_edge_storage")])
```

# Dash bugs
## get_nodes()
NOTE: get_nodes() does not work (25.06.2026.), does not filter edges
```
tree = cyto.utils.Tree(elements)
nodes = tree.get_nodes()[0]['data']['id'] 
```