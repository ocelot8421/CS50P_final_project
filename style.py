stylesheet = [
    # Group selectors
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)'
            #'content': 'data(label_hun)'
        }
    },

    # Class selectors
    {
        'selector': '.red',
        'style': {
            'background-color': 'red',
            'line-color': 'red'
        }
    },
    {'selector': '.pink',   'style': {'background-color': 'pink'}},
    {'selector': '.green',  'style': {'background-color': 'green'}},
    
    # Study NOTE: https://www.w3schools.com/cssref/css_colors.php    
    {'selector': '.cornsilk',
     'style': {'background-color': '#FFF8DC'}},
    {'selector': '.darkSeaGreen', 'style': {
         'background-color': '#8FBC8F', 'line-color': '#8FBC8F',
    }},
    
    {
        'selector': '.triangle',
        'style': {
            'shape': 'triangle'
        }
    },
    
    # Condition selektor
    {
        'selector': 'edge',
        'style': {
            'line-color': '#8FBC8F',
            'curve-style': 'bezier',
            'source-arrow-shape': 'circle',
            'source-arrow-color': '#8FBC8F',
        }
    },
    
    # Picture
    {
        'selector': '.large_picture',
        'style': {
            'width': 120,
            'height': 107,
            'background-fit': 'cover',
            'background-image': 'data(picture)'
        }
    },
    {
        'selector': '.medium_picture',
        'style': {
            'width': 90,
            'height': 80,
            'background-fit': 'cover',
            'background-image': 'data(picture)'
        }
    }
]

default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'line-color': '#A3C4BC'
        }
    }
]