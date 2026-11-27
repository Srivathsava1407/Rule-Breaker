import random

from pyscript import web, when
import rules

# establish the current rule as None at the start of the game
current_rule = None

hearts = 5

round_objects = []
matching_count = 0
correct_selected = 0
selected_difficulty = None
round_active = False
game_over = False


# define event handler for difficulty selection click
@when("click", ".content")
def choose_difficulty(event):
    global current_rule, selected_difficulty, round_active

    selected_difficulty = event.target.getAttribute("id")
    round_active = False

    web.page["difficulty"].textContent = selected_difficulty

    if selected_difficulty == "Easy":
        current_rule = random.choice(rules.EASY_RULES)
    elif selected_difficulty == "Medium":
        current_rule = random.choice(rules.MEDIUM_RULES)
    elif selected_difficulty == "Hard":
        current_rule = random.choice(rules.HARD_RULES)

    show_history()

# define the event handler for the start button click
@when("click", "#start-button")
def start_game(event):
    global round_objects, matching_count, correct_selected, hearts, current_rule, round_active, game_over

    hearts = 5
    game_over = False
    set_hamster("sweet", "A cheerful hamster idle")
    round_objects, matching_count = generate_round(current_rule)
    correct_selected = 0
    show_objects(round_objects)
    web.page["game-message"].textContent = "Choose an object."
    web.page["objects"].hidden = False
    web.page["lives"].hidden = False
    web.page["hearts"].textContent = hearts * "❤️"
    web.page["correct-history-objects"].innerHTML = ""
    web.page["wrong-history-objects"].innerHTML = ""

    round_active = True
    show_history()

# define the event handler for the object selection click
def choose_object(event):
    global current_rule, hearts, correct_selected, selected_item, game_over

    if current_rule is None or game_over:
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
COLORS = ["#FF746C", "#9FDDD0", "#B5DAED", "#FFDC82", "#A290B7"]
SIZES = ["small", "big"]
OBJECT_COUNT = 15
SVG_SHAPES = ["hexagon", "square", "triangle", "circle"]

def matches_rule(item, rule):
    for condition in rule["conditions"]:
        value = item[condition["attribute"]]

        if condition.get("operator", "equals") == "even":
            if value % 2 != 0:
                return False
        elif value != condition["value"]:
            return False

    return True

def generate_round(rule):
    conditions = rule["conditions"]
    if not conditions:
        raise ValueError("A rule must have at least one condition.")

    items = [
        {
            "color": random.choice(COLORS),
            "size": random.choice(SIZES),
            "shape": random.choice(SVG_SHAPES),
            "number": random.randint(1, 100),
            "selected": False,
        }
        for _ in range(OBJECT_COUNT)
    ]

    matching_count = random.randint(2, OBJECT_COUNT - 5)
    matching_indexes = set(random.sample(range(OBJECT_COUNT), matching_count))

    # Make the matching objects satisfy all conditions.
    for index in matching_indexes:
        item = items[index]
        for condition in conditions:
            attribute = condition["attribute"]

            if condition.get("operator", "equals") == "even":
                item[attribute] = random.choice(range(2, 101, 2))
            else:
                item[attribute] = condition["value"]

    # Make every other object fail the first condition.
    condition = conditions[0]
    attribute = condition["attribute"]

    if condition.get("operator", "equals") == "even":
        failing_values = list(range(1, 101, 2))
    else:
        possible_values = {
            "color": COLORS,
            "size": SIZES,
            "shape": SVG_SHAPES,
            "number": range(1, 101),
        }.get(attribute)

        if possible_values is None:
            raise ValueError(f"Unsupported rule attribute: {attribute}")

        failing_values = [
            value for value in possible_values
            if value != condition["value"]
        ]

    if not failing_values:
        raise ValueError(f"Cannot create a non-matching object for {attribute}.")

    for index, item in enumerate(items):
        if index not in matching_indexes:
            item[attribute] = random.choice(failing_values)

    return items, matching_count

# code function to display the randomly generated objects
SHAPE_FILES = {
    "hexagon": "object_shapes/hexagon.svg",
    "square": "object_shapes/square.svg",
    "triangle": "object_shapes/triangle.svg",
    "circle": "object_shapes/circle.svg"
}

SHAPES = list(SHAPE_FILES)

def show_objects(items):
    container = web.page["objects"]
    container.innerHTML = ""

    for index, item in enumerate(items):
        size = "6rem" if item["size"] == "big" else "4rem"
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

# function to check the display condition for the history section
def show_history():
    is_hard = selected_difficulty == "Hard"
    toggle = web.page["show-history-toggle"]
    checkbox = web.page["check"]

    toggle.hidden = is_hard

    if is_hard:
        checkbox.checked = False

    web.page["history"].hidden = (
        is_hard or not round_active or not checkbox.checked
    )

@when("change", "#check")
def history_toggle_changed(event):
    show_history()

from js import document

def open_credits_modal(event=None):
    modal = document.getElementById("modal-credits")
    if modal:
        modal.showModal()

# function to define the hamster expression 
def set_hamster(expression, alt_text):
    image = web.page["hamster_image"]._dom_element
    image.setAttribute(
        "src",
        f"hamster_images/hamster_{expression}.webp"
    )
    image.setAttribute("all", alt_text)