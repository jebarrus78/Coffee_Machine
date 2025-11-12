# --- imports (remove unused) ---
# import random
import art
# import math

MENU = {
    "espresso": {
        "ingredients": {"water": 50, "coffee": 18},
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {"water": 200, "milk": 150, "coffee": 24},
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {"water": 250, "milk": 100, "coffee": 24},
        "cost": 3.0,
    },
}

# Emojis
water_emoji = "🚰"
coffee_emoji = "☕"
milk_emoji = "🐄"
danger_emoji = "☢️"
check_emoji = "🔎"
profit_emoji = "💸"

# Maximum Resources
MAX_RESOURCES = {"water": 300, "milk": 200, "coffee": 100}
profit = 0.0
resources = {"water": 300, "milk": 200, "coffee": 100}
def check_levels():
    return(f"{water_emoji} = {resources['water']}\n"
          f"{milk_emoji} = {resources['milk']}\n"
          f"{coffee_emoji} = {resources['coffee']}\n"
          f"{profit_emoji} = ${profit:.2f}")
def run_report():
    # fix quotes inside f-strings
    print(check_levels())
    # print(input("Replenish resources to max? (y/n): ").strip().lower())
    if input("\nReplenish resources to max? (y/n): ").strip().lower() == "y":
        replenish_resources()
    else:
        print("Resources not replenished.\n")

    if input("Press Enter to continue...").lower() == "n":
        print("Exiting report.")
    else:
        print("Continuing to main menu.\n")




def check_resources(current_resources):
    """Compare current vs max, show low warnings, and report what can’t be made."""
    print(f"\n{check_emoji} Resource Check Report:")
    low_threshold = 0.5

    for item, max_amount in MAX_RESOURCES.items():
        current = current_resources.get(item, 0)
        percent = current / max_amount if max_amount else 0

        if percent == 1:
            state = "Full"
        elif percent >= low_threshold:
            state = "Sufficient"
        elif percent > 0:
            state = "Low"
        else:
            state = f"Empty {danger_emoji}"

        print(f"{item}: {current}/{max_amount} ({state})")

    # What can't be made with current resources:
    cannot = []
    for drink, data in MENU.items():
        ok = True
        for item, amt in data["ingredients"].items():
            if current_resources.get(item, 0) < amt:
                ok = False
                break
        if not ok:
            cannot.append(drink)
    if cannot:
        print("Cannot prepare:", ", ".join(cannot))
    else:
        print("All drinks can be prepared.\n")

options = {
    "1": "espresso",
    "2": "latte",
    "3": "cappuccino",
    "4": "report",
    "5": "off",
}

def get_user_choice():
    valid_choices = list(options.keys()) + ["report", "off"]
    while True:
        print(art.logo)
        choice = input(
            "What would you like?\n"
            f"1) {coffee_emoji} Espresso\n"
            f"2) {coffee_emoji} Latte\n"
            f"3) {coffee_emoji} Cappuccino\n"
            f"4) {check_emoji} Run Report\n"
            f"5) {danger_emoji} Turn Off\n> "
        ).lower().strip()

        if choice in valid_choices:
            if choice in options:
                return options[choice]  # mapped value
            else:
                return choice           # typed 'report' or 'off'
        print("Invalid choice. Please try again.")

def replenish_resources():
    print("Replenishing resources...")
    for item in resources:
        resources[item] = MAX_RESOURCES[item]
    print("Resources replenished to maximum.")

def turn_off_machine():
    print("Turning off the coffee machine...")
    raise SystemExit

def check_sufficient_resources(drink):
    """Check if there are enough resources to make the drink."""
    ingredients = MENU[drink]["ingredients"]
    for item, amount in ingredients.items():
        if resources.get(item, 0) < amount:
            print(f"Sorry, not enough {item}.")
            return False
    return True

def process_coins():
    print("\nPlease insert coins.")
    total = 0.0
    try:
        total += int(input("How many quarters? ")) * 0.25
        total += int(input("How many dimes? ")) * 0.10
        total += int(input("How many nickels? ")) * 0.05
        total += int(input("How many pennies? ")) * 0.01
    except ValueError:
        print("Invalid coin entry. Refunding.")
        return 0.0
    return round(total, 2)

def check_transaction(drink, payment):
    global profit
    cost = MENU[drink]["cost"]
    if payment >= cost:
        change = round(payment - cost, 2)
        print(f"Transaction successful. Your change is ${change}.")
        profit += cost
        return True
    else:
        print("Sorry, that's not enough money. Money refunded.")
        input("Press Enter to continue...\n")
        print("\n"*20)
        return False

def make_coffee(drink):
    ingredients = MENU[drink]["ingredients"]
    for item, amount in ingredients.items():
        resources[item] -= amount
    print(f"Here is your {drink}. Enjoy!")

def main():
    print("Coffee Machine Ready.")
    run_report()
    check_resources(resources)
    print(art.logo)

    while True:
        choice = get_user_choice()

        if choice == "off":
            turn_off_machine()
        elif choice == "report":
            run_report()
            check_resources(resources)
        elif choice in {"espresso", "latte", "cappuccino"}:
            if not check_sufficient_resources(choice):
                ask = input("Replenish resources to max? (y/n): ").strip().lower()
                if ask == "y":
                    replenish_resources()
                else:
                    continue

            payment = process_coins()
            if check_transaction(choice, payment):
                make_coffee(choice)
        else:
            print("Unknown option. Try again.")

if __name__ == "__main__":
    main()
