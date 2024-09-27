from dataclasses import dataclass

from pymongo.collection import Collection

from recipe import Recipe


@dataclass
class RecipeRepository:
    collection: Collection

    def add(self, recipe: Recipe):
        self.collection.insert_one(recipe.to_dict())

    def add_all(self, recipes: list):
        self.collection.insert_many(recipes)

    def delete_all(self) -> None:
        self.collection.delete_many({})

    def average_number_of_ingredients(self) -> float:
        cursor = self.collection.aggregate(
            [
                {"$project": {"num_ingredients": {"$size": "$Ingredients"}}},
                {"$group": {"_id": None, "average": {"$avg": "$num_ingredients"}}},
            ]
        )
        result: dict = next(cursor, {})
        return round(result.get("average", 0), 2)

    def average_preparation_steps(self) -> float:
        cursor = self.collection.aggregate(
            [
                {"$project": {"num_steps": {"$size": "$Cooking Steps"}}},
                {"$group": {"_id": None, "average": {"$avg": "$num_steps"}}},
            ]
        )
        result: dict = next(cursor, {})

        return round(result.get("average", 0), 2)

    def recipe_with_most_servings(self) -> Recipe:
        result = self.collection.find({}, {"_id": 0}).sort("Portion", -1).limit(1)
        return Recipe.from_dict(result[0])

    def author_with_most_recipes(self) -> tuple[str, int]:
        cursor = self.collection.aggregate(
            [
                {"$group": {"_id": "$Author", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 1},
                {"$project": {"_id": 0, "author": "$_id", "count": 1}},
            ]
        )
        result = next(cursor, None)
        if result is not None:
            return result["author"], result["count"]

        return "", 0
