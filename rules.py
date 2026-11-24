import random

COLORS = ["#FF746C", "#9FDDD0", "#B5DAED", "#FFDC82", "#A290B7"]

RULES = [
    {"prompt": "Choose the red object", "correct_color": "red"},
    {"prompt": "Choose the blue object", "correct_color": "blue"},
    {"prompt": "Choose the green object", "correct_color": "green"},
    {"prompt": "Choose the yellow object", "correct_color": "yellow"}
]

random_color = random.choice(COLORS)

EASY_RULES = [
    {"prompt": f"Choose the {random_color} objects", "attribute": "color", "value": random_color},
    {"prompt": "Choose the small objects", "attribute": "size", "value": "small"},
    {"prompt": "Choose the big objects", "attribute": "size", "value": "big"}
]

MEDIUM_RULES = [
    {
        "prompt": f"Choose the small {random_color} objects",
        "conditions": [
            {"attribute": "size", "value": "small"},
            {"attribule": "color", "value": random_color}
        ]
    },
    {
        "prompt": f"Choose the big {random_color} objects",
        "conditions": [
            {"attribute": "size", "value": "big"},
            {"attribule": "color", "value": random_color}
        ]
    }
]

HARD_RULES = [
    {"prompt": "Choose objects showing the number 7", "attribute": "number", "value": 7},
]