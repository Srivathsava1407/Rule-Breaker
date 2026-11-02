import random

from pyscript import web, when
from rules import RULES

# establish the current rule as None at the start of the game
current_rule = None

hearts = 3

# define the event handler for the start button click
@when("click", "#start-button")
def start_game(event):
    global current_rule
    global hearts

    current_rule = random.choice(RULES)
    #web.page["game-rule"].textContent = current_rule["prompt"]
    web.page["game-message"].textContent = "Choose an object."
    web.page["objects"].hidden = False
    web.page["lives"].hidden = False
    web.page["hearts"].textContent = hearts * "❤️"

# define the event handler for the object selection click
@when("click", ".object")
def choose_object(event):
    global current_rule
    global hearts

    if current_rule is None:
        return

    selected_color = event.target.getAttribute("data-color")  # obtaining what the user has selected

    if selected_color == current_rule["correct_color"]:
        web.page["game-message"].textContent = "Correct! You Win."
        current_rule = None
    else:
        web.page["game-message"].textContent = "Not that one. Try again"
        hearts -= 1
        web.page["hearts"].textContent = hearts * "❤️"
        if hearts == 0:
            web.page["game-message"].textContent = "You Lose!"