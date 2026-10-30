import random

from pyscript import web, when
from rules import RULES

current_rule = None

@when("click", "#start-button")
def start_game(event):
    global current_rule

    current_rule = random.choice(RULES)
    #web.page["game-rule"].textContent = current_rule["prompt"]
    web.page["game-message"].textContent = "Choose an object."
    web.page["objects"].hidden = False

@when("click", ".object")
def choose_object(event):
    global current_rule

    if current_rule is None:
        return

    selected_color = event.target.getAttribute("data-color")

    if selected_color == current_rule["correct_color"]:
        web.page["game-message"].textContent = "Correct! You win."
        current_rule = None
    else:
        web.page["game-message"].textContent = "Not that one."