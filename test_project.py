import project

def test_read_map():
    assert project.read_map("test_csv_input.csv") == [{'data': {'id': 'one', 'label': 'relax in the garden'}, 'position': {'x': 75, 'y': 75}}, {'data': {'id': 'two', 'label': 'swipe up trash'}, 'position': {'x': 200, 'y': 200}}, {'data': {'source': 'one', 'target': 'two'}}]