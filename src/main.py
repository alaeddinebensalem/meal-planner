import math
import database, utils
from collections import defaultdict

COL_WIDTH = 40
RECIPES_PER_LINE = 5

main_menu_text = """Please select one of the following options:
1) Create a mean plan.
2) Add new recipe.
3) Add new ingredient.
4) Add new Location.
5) Exit
"""

ingredient_dict = {}
recipe_dict = {}
location_dict = {}


# menus
def main_menu():
    while (user_choice := input(main_menu_text)) != '5':
        if user_choice == '1':
            meal_plan_menu()
        elif user_choice == '2':
            add_recipe_menu()
        elif user_choice == '3':
            add_new_ingredient_menu()
        elif user_choice == '4':
            add_new_location_menu()
        else:
            print("Invalid input!")


def meal_plan_menu():
    global recipe_dict
    recipe_dict = utils.map_dict(database.get_all_recipes())
    recipes = []
    recipe_id = {}

    while True:
        if recipes:
            print_meal_selection(recipes)
        print("Please select the number of the recipe to add or 'finish' or 'exit': ")
        print_recipes()
        user_choice = utils.input_int("Your Selection: ", len(recipe_dict), ("finish", "exit"))
        if user_choice == 'finish':
            generate_shopping_list(recipes)
            return

        if user_choice == 'exit':
            exit()
        recipes.append(recipe_dict[user_choice])


def add_recipe_menu():
    while True:
        name = input("Please enter the name of the recipe or 'exit': ")
        if name.lower() == "exit":
            exit()
        id_ = database.check_recipe_id(name)
        if id_ != -1:
            print("Recipe already exists! Please enter a new recipe.")
        else:
            break

    print("Please enter the ingredients of the recipe: ")
    ingredients = []
    while True:
        print_ingredients()
        ing_num = utils.input_int("\nEnter ingredient number or 'finish' to finish or 'exit' to exit: ",
                                  len(ingredient_dict), ('exit', 'finish'))
        if ing_num == "exit":
            exit()
        if ing_num == 'finish':
            if ingredients:
                break
            else:
                print("A recipe must include at least one ingredient")
                continue
        amount = float(input("Enter amount of ingredients up to 3 decimal places: "))
        ingredients.append((ingredient_dict[ing_num][0], amount))
    id_ = database.get_recipe_id(name)
    for ing_id, amount in ingredients:
        database.add_recipe_ingredient((id_, ing_id, amount))


def add_new_location_menu():
    location = input("Please enter the name of the location: ")
    database.add_location(location)


def add_new_ingredient_menu():
    name = input("Please enter the name of the ingredient: ")
    unit = input("Enter the unit for this ingredient: ")
    p_unit = input("Please enter the minimum purchase unit of is ingredient: ")
    print_locations()
    location_num = utils.input_int("Enter the location number: ", len(location_dict))
    database.add_ingredient((name, unit, p_unit, location_dict[location_num][0]))


# print methods
def print_ingredients():
    print("\nIngredients:")
    global ingredient_dict
    ingredient_dict = utils.map_dict(database.get_all_ingredients())
    for local_id, (_, ingredient) in ingredient_dict.items():
        print(f"{local_id}: {ingredient}")


def print_locations():
    global location_dict
    print("\nLocations:")
    location_dict = utils.map_dict(database.get_all_locations())
    for local_id, (_, location) in location_dict.items():
        print(f"{local_id}: {location}")


def print_recipes():
    global recipe_dict
    recipe_dict = utils.map_dict(database.get_all_recipes())
    for local_id, (_, recipe) in recipe_dict.items():
        print(f"{local_id}: {recipe:<{COL_WIDTH}}", end="")
        if local_id % 3 == 0:
            print()


def print_meal_selection(recipes):
    print("Your current selected recipes are: ")
    count = 0
    for r in recipes[:-1]:
        if count and count % RECIPES_PER_LINE == 0:
            print()
        count += 1

        print(f"\033[1m{r[1]} | \033[0m", end="")
    print(f"\033[1m{recipes[-1][1]}\033[0m")


def generate_shopping_list(recipes):
    recipes_ingredients = defaultdict(lambda: defaultdict(float))
    pu_dict = {}
    unit_dict = {}
    for id_, _ in recipes:
        ingredients = database.get_recipe_ingredient(id_)
        for name, amount, purchase_amount, unit, location in ingredients:
            recipes_ingredients[location][name] += float(amount)
            pu_dict[name] = float(purchase_amount)
            unit_dict[name] = unit

    shopping_list = defaultdict(set)
    for location in recipes_ingredients:
        for name, amount in recipes_ingredients[location].items():
            pu = pu_dict.get(name, 1) or 1
            adj_amount = math.ceil(amount / pu) * pu
            unit = unit_dict[name] if unit_dict[name] else ""
            shopping_list[location].add(f"  - {name}: {adj_amount} {unit}")

    for location in shopping_list:
        print(f"\033[1m{location}:\033[0m")
        for item in shopping_list[location]:
            print(item)


main_menu()
