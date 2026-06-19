import json

from project import get_all_nodes, get_all_leaves

def test_collect_nodes():
    with open("gardening_test.json") as test_file:
        test_json = json.load(test_file)
    with open("gardening_test.json") as test_nodes_file:
        test_node_json = json.load(test_nodes_file)
    assert get_all_nodes(test_json) == test_node_json
    
# def test_collect_leaves(): TODO
#     with open("gardening_test.json") as test_file:
#         test_json = json.load(test_file)
#     with open("gardening_test_leaves.json") as test_nodes_file:
#         test_node_json = json.load(test_nodes_file)
#     assert get_all_leaves(test_json) == test_node_json