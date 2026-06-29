import json

from project import get_all_nodes, get_all_leaves, find_root

def get_json_elements(json_file):
    with open(json_file) as test_file:
        json_elements = json.load(test_file)
    return json_elements

def test_collect_nodes():
    json_elements = get_json_elements("gardening_test.json")
    test_node_json = get_json_elements("gardening_test_nodes.json")
    assert get_all_nodes(json_elements) == test_node_json
    
def test_collect_leaves():
    json_elements = get_json_elements("gardening_test.json")
    json_leaves = get_json_elements("gardening_test_leaves.json")
    assert get_all_leaves(json_elements) == json_leaves
    
def test_get_root():
    json_elements = get_json_elements("gardening_test.json")
    json_tapNodeData = get_json_elements("gardening_test_one_node.json")
    assert find_root(json_elements, json_tapNodeData) == "Goal > > > Relax in the garden"