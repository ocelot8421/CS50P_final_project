import base64
import json
from PIL import Image

import id


# NOTE:
# https://en.wikipedia.org/wiki/Data_URI_scheme
# https://js.cytoscape.org/#style/background-image
# https://bobbyhadz.com/blog/convert-image-to-base64-string-in-python
# https://dash.plotly.com/cytoscape/styling
def encode_pic(pic_name):
    path = "pictures/" + pic_name
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:image/jpg;base64,{encoded}"

default_gardening_elements=[
    {
        'data': {
            'id': id.GARDENRELAX,
            'label': 'Relax in the garden',
            'label_hun': 'Relaxálás a kertben',
            'picture': encode_pic("gardenrelax.jpg")
        },
        'position': {'x': 0, 'y': 0},
        'classes': 'large_picture',
    },
    {
        'data': {
            'id': id.SWEEPING,
            'label': 'Swiping the yard',
            'label_hun': 'Udvar felseprése',
            'picture': encode_pic("sweeping_yard.png")
        },
        'position': {'x': 40, 'y': 130},
        'classes': 'medium_picture'
    },
    {
        'data': {
            'id': id.PAVER_WEEDING,
            'label': 'Paver weeding',
            'label_hun': 'Térkő gazolása',
            'picture': encode_pic("pavernweeding.png")
        },
        'position': {'x': -50, 'y': 230},
        'classes': 'medium_picture'
    },
    {
        'data': {
            'id': id.POLYMERSAND,
            'label': 'Polymer-stabilized sand',
            'label_hun': 'Polimer fugahomok',
            'picture': encode_pic("polymer_sand.png")
        },
        'position': {'x': 60, 'y': 340},
        'classes': 'medium_picture'
    },
    {
        'data': {
            'id': id.WATERING,
            'label': 'Watering',
            'label_hun': 'Locsolás',
            'picture': encode_pic("watering.png")
        },
        'position': {'x': 190, 'y': 70},
        'classes': 'medium_picture'
    },
    {'data': {'source': id.GARDENRELAX, 'target': id.SWEEPING}},
    {'data': {'source': id.SWEEPING, 'target': id.PAVER_WEEDING}},
    {'data': {'source': id.PAVER_WEEDING, 'target': id.POLYMERSAND}},
    {'data': {'source': id.GARDENRELAX, 'target': id.WATERING}},
]

# Read user elements from json
# Study NOTE: https://realpython.com/python-json/#:~:text=json.load(read_file)
# try:
#     with open("gardening_user.json", mode="r", encoding="utf-8") as read_user_file:
#         user_elements = json.load(read_user_file)
# except FileNotFoundError:
#     with open("gardening.json", mode="r", encoding="utf-8") as read_file:
#         user_elements = json.load(read_file)
with open("gardening_user.json", mode="r", encoding="utf-8") as read_user_file:
    user_elements = json.load(read_user_file)

# Encode pictures
for element in user_elements:
    try:
        pic_name = element['data']['picture']
        element['data']['picture'] = encode_pic(pic_name)
    except:
        continue


