"""
https://dash.plotly.com/cytoscape
"""

import callbacks
import id
import dash_cytoscape as cyto
from dash import Dash, html, dcc
from dash import Input, Output, State, callback
from dash_extensions import EventListener
from elements import default_gardening_elements as gardening_steps
from style import stylesheet

# NOTE for study: https://docs.python.org/3/library/pprint.html#module-pprint
from pprint import pprint



def main():

    app = Dash()

    # NOTE for study: https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent/clientX
    event = {
        "event": "click",
        "props": ["clientX", "clientY", "timeStamp"]
    }

    # NOTE for study: https://dash.plotly.com/dash-core-components/store
    app.layout = html.Div([
        dcc.Store(id="new_node_storage", storage_type='session'),
        cyto.Cytoscape(
            id=id.CYTOSCPE,
            layout={'name': 'preset'},
            style={'width': '50%', 'height': '600px'},
            elements=gardening_steps,
            stylesheet=stylesheet
        ),
        dcc.Markdown(id=id.MARKDOWN_UPPER),
        dcc.Markdown(id="log_new_node_position"),
        dcc.Markdown(id=id.MARKDOWN_LOWER),
        EventListener(
            id=id.EVENTlISTENER_TEST,
            events=[event],
            logging=True
        )
    ])

    app.run(debug=True)



@callback(Output("log_new_node_position", "children"),
          Input(id.EVENTlISTENER_TEST, "n_events"),
          Input(id.EVENTlISTENER_TEST, "event"),
          State(id.CYTOSCPE, 'tapNode'))
def click_event(n_events, e, tapNode):
    if not tapNode:
        return f"* click: \n {e}"
    return f"* click: \n {e} \n* tapNode: {tapNode['renderedPosition']}{tapNode['timeStamp']}"


@callback(Output(id.CYTOSCPE, 'elements'),
          State(id.CYTOSCPE, 'elements'),
          State("new_node_storage", "data"),
          Input(id.EVENTlISTENER_TEST, "event"),
          prevent_initial_call=True)
def insert_new_node(elements, storage, event):
    
    try:
        ids = set()
        for element in elements:
            ids.add(element['data']['id'])

        if storage['new_node']['id'] not in ids and storage['new_node']['position'] != {}:
            elements.extend([
                {
                    'data': {
                        'id': storage['new_node']['id'],
                        'label': storage['new_node']['label'],
                        'label_hun': storage['new_node']['label_hun'],
                    },
                    'position': storage['new_node']['position'],
                    'classes': 'medium_picture'
                }])
            storage['new_node'] = {
                'id': '',
                'triple_clicked': 0,
                'triple_tapped': 0,         # TODO rename
                'position': {}
            }
            storage['clicks'] = []
            storage['tapNodes'] = []
    except:
        raise ValueError("empty new node")



    return elements

@callback(Output("new_node_storage", "data"),
          State("new_node_storage", "data"),
          Input(id.CYTOSCPE, 'tapNode'),
          Input(id.EVENTlISTENER_TEST, "event"),
          prevent_initial_call=True)
def calculate_new_node_position(storage, tapNode, click):

    ## Check for existing storage
    if storage:

        ## Check triple click on empty space

        # Prepare trashhold, click list and flag, new_node_dict
        try:
            if click['clientX'] - tapNode['renderedPosition']['x'] > 50 or click['clientY'] - tapNode['renderedPosition']['y'] > 50:
                storage['clicks'].append(click)
        except:
            raise ValueError("no tapnode")

        # There have to be the latest 3 clicks (not tap on node) in the storage
        if len(storage['clicks']) > 3:
            storage['clicks'].pop(0)

            # Get two consecutive clicks at once
            for i in range(2):
                click_i0, click_i1 = storage['clicks'][i], storage['clicks'][i+1]

                # Check distance between click coordinate
                dX, dY = click_i1['clientX']-click_i0['clientX'], click_i1['clientY']-click_i0['clientY']
                if abs(dX) > 30 or abs(dY) > 30: break

                # Check time differnce between clicks
                if click_i1['timeStamp']-click_i0['timeStamp'] > 3000: break

                # Turn triple clicked flag True if everything okay
                storage['new_node']['triple_clicked'] += 1

        ## check two tap on not same node
        if tapNode:
            actual_tapNode = {
                'timeStamp': tapNode['timeStamp'],
                'renderedPosition': tapNode['renderedPosition'],
                'position': tapNode['position']
            }
            nds = storage['tapNodes']
            try:
                if len(nds) == 0 or (nds[len(nds)-1]['position'] != actual_tapNode['position']):
                    storage['tapNodes'].append(actual_tapNode)
            except:
                raise ValueError("empty")


        if len(storage['tapNodes']) > 4:
            storage['tapNodes'].pop(0)
            tap_0, tap_1, tap_2, tap_3 = [i for i in storage['tapNodes']]

            if tap_0['position'] == tap_2['position']: # TODO refactor
                storage['new_node']['triple_tapped'] += 1
            else:
                storage['new_node']['triple_tapped'] = 0

            if tap_1['position'] == tap_3['position']:
                storage['new_node']['triple_tapped'] += 1
            else:
                storage['new_node']['triple_tapped'] = 0

            # Calculate new node position
            if storage['new_node']['triple_tapped'] >= 2 and storage['new_node']['triple_clicked'] >= 3:
                x00, y00 = tap_0['position']['x'], tap_0['position']['y']
                x01, y01 = tap_1['position']['x'], tap_1['position']['y']
                xr00, yr00 = tap_0['renderedPosition']['x'], tap_0['renderedPosition']['y']
                xr01, yr01 = tap_1['renderedPosition']['x'], tap_1['renderedPosition']['y']
                xrc, yrc = storage['clicks'][0]['clientX'], storage['clicks'][0]['clientY']
                dxr_01_00, dyr_01_00 = xr01-xr00, yr01-yr00
                dx_01_00, dy_01_00 = x01-x00, y01-y00
                dxr_c_00, dyr_c_00 = xrc-xr00, yrc-yr00
                storage['new_node']['position']['x'] = int(x00 + dxr_c_00 * dx_01_00 / dxr_01_00)
                storage['new_node']['position']['y'] = int(y00 + dyr_c_00 * dy_01_00 / dyr_01_00)


        ## Check minimal distance between triple-click and triple-tap (last events via index 2)
        clcik_list = storage['clicks']
        if len(storage['clicks']) == 3 and len(storage['tapNodes']) == 4:
            cX, cY, c_time_short = clcik_list[2]['clientX'], clcik_list[2]['clientY'], str(clcik_list[2]['timeStamp'])[0:6]

            ## Make new node if triple-click and triple click are True
            if storage['new_node']['triple_tapped'] >= 2 and storage['new_node']['triple_clicked'] >= 3:
                storage['new_node']['id'] = f"{cX}_{cY}_{c_time_short}"
                storage['tapNodes'] = []
                storage['new_node']['triple_clicked'] = 0
                storage['new_node']['triple_tapped'] = 0
                storage['new_node']['label'] = "New node"
                storage['new_node']['label_hun'] = "Új mező"
                storage['new_node']['classes'] = "medium_picture"


    ## Init storage
    else:
        storage = {
            'clicks': [],
            'tapNodes': [],
            'new_node': {
                'id': '',
                'triple_clicked': 0,
                'triple_tapped': 0,         # TODO rename
                'position': {}
            }
        }

    return storage


if __name__ == '__main__':
    main()