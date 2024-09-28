from parser import recipe_list

from pymongo import MongoClient

from recipe_repository import RecipeRepository

COLLECTION_NAME = "recipes"
DATABASE_NAME = "recipe_database"
USER = ""  # enter your username for MongoDB user
PASSWORD = ""  # enter your password


def main():
    client = MongoClient(f"mongodb://{USER}:{PASSWORD}@localhost:27017")
    database = client[DATABASE_NAME]

    recipes_collection = database[COLLECTION_NAME]

    recipe_repository = RecipeRepository(recipes_collection)
    recipe_repository.delete_all()

    recipe_repository.add_all(recipe_list)

    avg_ingredients = recipe_repository.average_number_of_ingredients()
    print(f"\nAverage number of ingredients per recipe is {avg_ingredients}.")

    avg_steps = recipe_repository.average_preparation_steps()
    print(f"\nAverage number of preparation steps per recipe is {avg_steps}.")

    recipe = recipe_repository.recipe_with_most_servings()
    print(f"\nRecipe with most servings is {recipe.title} ({recipe.url}).")

    author, recipe_count = recipe_repository.author_with_most_recipes()
    print(f"\nAuthor with most recipes is {author} with {recipe_count} recipes.")


if __name__ == "__main__":
    main()
