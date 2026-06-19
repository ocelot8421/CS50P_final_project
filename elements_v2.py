default_gardening_elements=[
    {
        'data': {
            'id': 'GARDENRELAX',
            'label': 'Relax in the garden',
            'label_hun': 'Relaxálás a kertben',
        },
        'position': {'x': 0, 'y': 0},
        'classes': 'large_picture',
    },
    {
        'data': {
            'id': 'SWEEPING',
            # 'label': 'Swiping the yard',
            'label': 'Ice cream eating',
            'label_hun': 'Udvar felseprése',
        },
        'position': {'x': 40, 'y': 130},
        'classes': 'medium_picture'
    },
    {
        'data': {
            'id': 'ghjk',
            # 'label': 'Swiping the yard',
            'label': 'Ice cream eating',
            'label_hun': 'Udvar felseprése'
        },
        'position': {'x': 40, 'y': 130},
        'classes': 'medium_picture'
    },
    {
        'data': {
            'id': 'PAVER_WEEDING',
            'label': 'Paver weeding',
            'label_hun': 'Térkő gazolása',
        },
        'position': {'x': -50, 'y': 230},
        'classes': 'medium_picture'
    },
    {
        'data': {
            'id': 'POLYMERSAND',
            'label': 'Polymer-stabilized sand',
            'label_hun': 'Polimer fugahomok',
        },
        'position': {'x': 60, 'y': 340},
        'classes': 'medium_picture'
    },
    {
        'data': {
            'id': 'WATERING',
            'label': 'Watering',
            'label_hun': 'Locsolás',
        },
        'position': {'x': 190, 'y': 70},
        'classes': 'medium_picture'
    },
    {'data': {'source': 'GARDENRELAX', 'target': 'SWEEPING'}},
    {'data': {'source': 'SWEEPING', 'target': 'PAVER_WEEDING'}},
    {'data': {'source': 'PAVER_WEEDING', 'target': 'POLYMERSAND'}},
    {'data': {'source': 'GARDENRELAX', 'target': 'WATERING'}},
]