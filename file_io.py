# def save_elements_into_python_file(elements, file_name):
        
#     with open(file_name, mode="w", encoding="utf-8") as output_file:
#             output_file.write("default_gardening_elements = [\n")
#             for element in elements:
#                 output_file.write("    " + str(element)+ ",\n")                
#             output_file.write("]")

import os
import json
from platformdirs import user_data_dir


DEFAULT_JSON = os.path.join(os.path.dirname(__file__), "gardening_default.json") 
# DEFAULT_JSON = os.path.join(os.path.dirname(__file__), "gardening_test.json") # To peek test graph
# get data directory to save user graph
USER_DIR = user_data_dir("Mind_Graph_CS50P_final", "8ocelot")
USER_JSON = os.path.join(USER_DIR, "user_mind_map.json")
# USER_JSON = os.path.join(USER_DIR, "test_mind_map.json") # To peek test graph


import tempfile

def save_elements(elements):
    # os.makedirs(USER_DIR, exist_ok=True)
    # with open(USER_JSON, "w", encoding="utf-8") as f:
    #     json.dump(elements, f, indent=4, ensure_ascii=False)    
    os.makedirs(USER_DIR, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=USER_DIR, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(elements, f, indent=4, ensure_ascii=False)
        os.replace(tmp_path, USER_JSON)  # atomi csere, csak siker esetén
    except Exception:
        os.remove(tmp_path)
        raise
    
    
    

def load_elements():
    if not os.path.exists(USER_JSON):
        with open(DEFAULT_JSON, "r", encoding="utf-8") as defaults:
            default_elements = json.load(defaults)        
        return default_elements
    with open(USER_JSON, "r", encoding="utf-8") as f:
        return json.load(f)
    