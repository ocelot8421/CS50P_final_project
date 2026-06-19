001,"https://pypi.org/project/dash-extensions/0.0.68/#:~:text=example%20app%20above.-,EventListener,-The%20EventListener%20component"

"TREE: ---------------"
study NOTE: https://dash.plotly.com/cytoscape/reference#:~:text=is%20mutable%20overall).-,utils.Tree,-A%20class%20to
    tree = utils.Tree(elements.default_gardening_elements)
    print(str(tree.get_nodes())[:500])

SUTDY NOTE: https://dash.plotly.com/devtools#callback-graph

Input("keyboard", "n_keydowns"),
Study NOTE: https://github.com/emilhe/dash-extensions/issues/11#:~:text=%5BInput(%22keyboard%22%2C%20%22n_keydowns%22)%5D%2C

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