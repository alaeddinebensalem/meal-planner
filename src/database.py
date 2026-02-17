import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require')

CREATE_RECIPE_TABLE = """
    CREATE TABLE IF NOT EXISTS recipe (
    id SERIAL PRIMARY KEY,
    recipe_name VARCHAR(100) UNIQUE NOT NULL
    );
"""

CREATE_LOCATION_TABLE = """CREATE TABLE IF NOT EXISTS location (
    id SERIAL PRIMARY KEY,
    location_name VARCHAR(100) UNIQUE NOT NULL
    );"""

CREATE_INGREDIENTS_TABLE = """
    CREATE TABLE IF NOT EXISTS ingredient (
    id SERIAL PRIMARY KEY,
    ingredient_name VARCHAR(100) UNIQUE NOT NULL,
    unit VARCHAR(20) NOT NULL,
    purchase_unit DECIMAL(6,3),
    location_id INTEGER NOT NULL,
    FOREIGN KEY (location_id) REFERENCES location (id)
    );
"""

CREATE_RECIPE_INGREDIENTS_TABLE = """
CREATE TABLE IF NOT EXISTS recipe_ingredient (
    recipe_id INTEGER,
    ingredient_id INTEGER,
    amount DECIMAL(6,3) NOT NULL,
    PRIMARY KEY(recipe_id, ingredient_id),
    FOREIGN KEY (recipe_id) REFERENCES recipe (id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredient (id)
    );
    """

# Queries
INSERT_LOCATION = "INSERT INTO location (location_name) VALUES (%s) ON CONFLICT DO NOTHING;"
INSERT_INGREDIENT = """INSERT INTO ingredient (ingredient_name,unit,purchase_unit,location_id)
 VALUES (LOWER(%s),UPPER(%s),%s,%s) ON CONFLICT DO NOTHING;"""
SELECT_ALL_LOCATION = "SELECT id,location_name FROM location;"
INSERT_RECIPE_INGREDIENT = """ INSERT INTO recipe_ingredient (recipe_id,ingredient_id,amount)
VALUES (%s,%s,%s) ON CONFLICT DO NOTHING;"""
INSERT_Return_RECIPE = """INSERT INTO recipe (recipe_name)
VALUES (LOWER(%s)) ON CONFLICT DO NOTHING RETURNING id;"""
SELECT_RECIPE_ID = "SELECT id FROM recipe WHERE recipe_name = LOWER(%s);"
SELECT_ALL_INGREDIENTS = "SELECT id, ingredient_name FROM ingredient;"
SELECT_ALL_RECIPES = "SELECT id, recipe_name FROM recipe;"
SELECT_RECIPE_INGREDIENT = """
SELECT ingredient_name, amount, purchase_unit, unit, location_name FROM recipe_ingredient
INNER JOIN ingredient
ON recipe_ingredient.ingredient_id = ingredient.id
INNER JOIN location
ON location_id = location.id
where recipe_id = %s;
"""


# methods
def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_RECIPE_TABLE)
            cursor.execute(CREATE_LOCATION_TABLE)
            cursor.execute(CREATE_INGREDIENTS_TABLE)
            cursor.execute(CREATE_RECIPE_INGREDIENTS_TABLE)


create_tables()


# add methods
def add_location(location_name):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_LOCATION, (location_name,))


def add_ingredient(record):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_INGREDIENT, record)


def add_recipe_ingredient(record):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_RECIPE_INGREDIENT, record)


# get methods
def check_recipe_id(name):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_RECIPE_ID, (name,))
            rslt = cursor.fetchone()
            if rslt:
                return rslt[0]
            else:
                return -1


def get_recipe_id(name):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_Return_RECIPE, (name,))
            result = cursor.fetchone()
            return result[0]


def get_all_recipes():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_RECIPES)
            return cursor.fetchall()


def get_recipe_ingredient(recipe_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_RECIPE_INGREDIENT, (recipe_id,))
            return cursor.fetchall()


def get_all_locations():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_LOCATION)
            return cursor.fetchall()


def get_all_ingredients():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_INGREDIENTS)
            return cursor.fetchall()
