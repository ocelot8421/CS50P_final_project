001,"https://pypi.org/project/dash-extensions/0.0.68/#:~:text=example%20app%20above.-,EventListener,-The%20EventListener%20component"

"TREE: ---------------"
study NOTE: https://dash.plotly.com/cytoscape/reference#:~:text=is%20mutable%20overall).-,utils.Tree,-A%20class%20to
    tree = utils.Tree(elements.default_gardening_elements)
    print(str(tree.get_nodes())[:500])

SUTDY NOTE: https://dash.plotly.com/devtools#callback-graph

Input("keyboard", "n_keydowns"),
Study NOTE: https://github.com/emilhe/dash-extensions/issues/11#:~:text=%5BInput(%22keyboard%22%2C%20%22n_keydowns%22)%5D%2C


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

