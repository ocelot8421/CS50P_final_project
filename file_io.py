import csv

def read_map(csv_in): # TODO don't use csv, use python dict
    """Generate map (nodes and edges) from csv file
    Args:
        csv_in (str): name of csv file
    Returns:
        list[dictionaries]: elements for cytoscape to generate
    """
    elements=[]
    
    with open(csv_in, "r") as gardening:  
        reader = csv.DictReader(gardening)
        for row in reader:
            if row['type'] == "node":
                new_node = {'data': {'id': row['id'], 'label': row['label']}, 'position': {'x': int(row['x']), 'y': int(row['y'])}, 'classes': row['classes']}
                elements.append(new_node)
            elif row['type'] == "edge":
                new_edge = {'data': {'source': row['source'], 'target': row['target']}}
                elements.append(new_edge)
            else:
                print("Invalid data in gardening.csv")    
                        
    return elements