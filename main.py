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
    global current_rule, selected_difficulty

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
    global round_objects, matching_count, correct_selected, hearts, current_rule

    round_objects, matching_count = generate_round(current_rule)
    correct_selected = 0
    show_objects(round_objects)
    #web.page["game-rule"].textContent = current_rule["prompt"]
    web.page["game-message"].textContent = "Choose an object."
    web.page["objects"].hidden = False
    web.page["lives"].hidden = False
    web.page["hearts"].textContent = hearts * "❤️"
    web.page["history"].hidden = False
    web.page["correct-history-objects"].innerHTML = ""
    web.page["wrong-history-objects"].innerHTML = ""

# define the event handler for the object selection click
def choose_object(event):
    global current_rule, hearts, correct_selected, selected_item

    if current_rule is None:
        return

    # Finds the button even if an SVG or span inside was clicked:
    button = event.target.closest("button")
    if not button:
        return

    index = int(button.getAttribute("data-index"))
    selected_item = round_objects[index]

    if selected_item["selected"]:
        return

    is_correct = matches_rule(selected_item, current_rule)
    selected_item["selected"] = True

    if is_correct:
        web.page["game-message"].textContent = "Correct!"
        correct_selected += 1
        button.disabled = True
        if correct_selected == matching_count:
            web.page["game-message"].textContent = "You Win!"
            current_rule = None
    else:
        web.page["game-message"].textContent = "Not that one. Try again"
        button.disabled = True
        hearts -= 1
        web.page["hearts"].textContent = hearts * "❤️"
        if hearts == 0:
            web.page["game-message"].textContent = "You Lose!"

    history_inventory(is_correct, button)

# code to create random selection of objects according to current_rule
COLORS = ["red", "green", "blue", "yellow"]
SIZES = ["small", "big"]
OBJECT_COUNT = 10
SVG_SHAPES = ["hexagon", "square"]

def matches_rule(item, rule):
    return item[rule["attribute"]] == rule["value"]

def generate_round(rule):
    items = [
        {
            "color": random.choice(COLORS),
            "size": random.choice(SIZES),
            "shape": random.choice(SVG_SHAPES),
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
SHAPE_FILES = {
    "hexagon": "object_shapes/hexagon.svg",
    "square": "object_shapes/square.svg",
}

SHAPES = list(SHAPE_FILES)

def show_objects(items):
    container = web.page["objects"]
    container.innerHTML = ""

    for index, item in enumerate(items):
        size = "8rem" if item["size"] == "big" else "4rem"
        svg_path = SHAPE_FILES[item["shape"]]

        button = web.button("", classes=["object"])
        button.style["width"] = size
        button.style["height"] = size
        button.style["color"] = item["color"]
        button._dom_element.setAttribute("data-index", str(index))

        button.innerHTML = f"""
            <svg class="shape-svg" viewBox="0 0 576 576" aria-hidden="true">
                <use href="{svg_path}#shape"></use>
            </svg>
            <span class="object-number" aria-hidden="true">{item["number"]}</span>
        """

        container.append(button)
        when("click", button)(choose_object)

# function to display the past moves, showing the player which objects were accepted and which weren't in two different sections
def history_inventory(is_correct, clicked_button):
    destination_id = (
        "correct-history-objects"
        if is_correct
        else "wrong-history-objects"
    )
    destination = web.page[destination_id]

    clicked_button.disabled = True
    destination._dom_element.appendChild(clicked_button)


from js import document

def open_credits_modal(event=None):
    modal = document.getElementById("modal-credits")
    if modal:
        modal.showModal()
