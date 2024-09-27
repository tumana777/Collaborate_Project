from pymongo import MongoClient

from recipe_repository import RecipeRepository
from temp import RECIPES_LIST

COLLECTION_NAME = "recipes"
DATABASE_NAME = "recipe_database"
ADMIN = "admin"
PASSWORD = "admin"


def main():
    client = MongoClient(f"mongodb://{ADMIN}:{PASSWORD}@localhost:27017")
    database = client[DATABASE_NAME]

    recipes_collection = database[COLLECTION_NAME]

    recipe_repository = RecipeRepository(recipes_collection)
    recipe_repository.delete_all()

    # recipes_list = parser()
    recipes_list = RECIPES_LIST
    recipe_repository.add_all(recipes_list)

    avg_ingredients = recipe_repository.average_number_of_ingredients()
    print(f"Average number of ingredients per recipe is {avg_ingredients}\n")

    avg_steps = recipe_repository.average_preparation_steps()
    print(f"Average number of preparation steps per recipe is {avg_steps}\n")

    recipe = recipe_repository.recipe_with_most_servings()
    print(f"Recipe with most servings is {recipe.title}:")
    print(recipe)

    author, recipe_count = recipe_repository.author_with_most_recipes()
    print(f"\nAuthor with most recipes is {author} with {recipe_count} recipes")


if __name__ == "__main__":
    main()
