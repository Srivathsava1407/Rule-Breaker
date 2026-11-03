import random

from pyscript import web, when
import rules

# establish the current rule as None at the start of the game
current_rule = None

hearts = 5

round_objects = []
matching_count = 0
correct_selected = 0


# define event handler for difficulty selection click
@when("click", ".content")
def choose_difficulty(event):
    global current_rule

    selected_difficulty = event.target.getAttribute("id")

    web.page["difficulty"].textContent = selected_difficulty

    if selected_difficulty == "Easy":
        current_rule = random.choice(rules.EASY_RULES)
    elif selected_difficulty == "Medium":
        current_rule = random.choice(rules.MEDIUM_RULES)
    elif selected_difficulty == "Hard":
        current_rule = random.choice(rules.HARD_RULES)


# define the event handler for the start button click
@when("click", "#start-button")
def start_game(event):
    global current_rule
    global hearts
    global round_objects, matching_count, correct_selected

    round_objects, matching_count = generate_round(current_rule)
    correct_selected = 0
    show_objects(round_objects)
    #web.page["game-rule"].textContent = current_rule["prompt"]
    web.page["game-message"].textContent = "Choose an object."
    web.page["objects"].hidden = False
    web.page["lives"].hidden = False
    web.page["hearts"].textContent = hearts * "❤️"

# define the event handler for the object selection click
def choose_object(event):
    global current_rule
    global hearts
    global correct_selected

    if current_rule is None:
        return

    index = int(event.target.getAttribute("data-index"))
    selected_item = round_objects[index]  # obtaining what the user has selected

    if selected_item["selected"]:
        return

    if matches_rule(selected_item, current_rule):
        web.page["game-message"].textContent = "Correct!"
        correct_selected += 1
        selected_item["selected"] = True
        event.target.disabled = True
        if correct_selected == matching_count:
            web.page["game-message"].textContent = "You Win!"
            current_rule = None
    else:
        web.page["game-message"].textContent = "Not that one. Try again"
        selected_item["selected"] = True
        event.target.disabled = True
        hearts -= 1
        web.page["hearts"].textContent = hearts * "❤️"
        if hearts == 0:
            web.page["game-message"].textContent = "You Lose!"

# code to create random selection of objects according to current_rule
COLORS = ["red", "green", "blue", "yellow"]
SIZES = ["small", "big"]
SHAPES = ["circle", "square", "traiangle", "star"]
OBJECT_COUNT = 10

def matches_rule(item, rule):
    return item[rule["attribute"]] == rule["value"]

def generate_round(rule):
    items = [
        {
            "color": random.choice(COLORS),
            "size": random.choice(SIZES),
            "shape": random.choice(SHAPES),
            "number": random.randint(1, 9),
            "selected": False,
        }
        for i in range(OBJECT_COUNT)
    ]

    matching_count = random.randint(2, OBJECT_COUNT-2)
    matching_indexes = random.sample(range(OBJECT_COUNT), matching_count)

    for index in matching_indexes:
        items[index][rule["attribute"]] = rule["value"]

    return items, matching_count

# code function to display the randomly generated objects
def show_objects(items):
    container = web.page["objects"]
    container.innerHTML = ""

    for index, item in enumerate(items):
        button = web.button(
            str(item["number"]),
            classes = ["object", f"shape-{item['shape']}"],
        )
        button.style["background-color"] = item["color"]
        button.style["width"]  = "8rem" if item["size"] == "big" else "4rem"
        button.style["height"] = "8rem" if item["size"] == "big" else "4rem"
        button._dom_element.setAttribute("data-index", str(index))

        container.append(button)
        when("click", button)(choose_object)