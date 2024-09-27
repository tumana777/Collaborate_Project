from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass
class Recipe:
    title: str
    url: str
    main_category: Category
    sub_category: Category
    image_url: str
    description: str
    author: str
    servings: int
    ingredients: list
    cooking_steps: list

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data.get("Title", ""),
            url=data.get("Recipe URL", ""),
            main_category=Category.from_dict(data.get("Main Category", {})),
            sub_category=Category.from_dict(data.get("Subcategory", {})),
            image_url=data.get("Image URL", ""),
            description=data.get("Description", ""),
            author=data.get("Author", ""),
            servings=data.get("Portion", 0),
            ingredients=data.get("Ingredients", []),
            cooking_steps=data.get("Cooking Steps", []),
        )

    def __str__(self) -> str:
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False)

    def to_dict(self) -> dict:
        return {
            "Title": self.title,
            "Recipe URL": self.url,
            "Main Category": self.main_category.to_dict(),
            "Subcategory": self.sub_category.to_dict(),
            "Image URL": self.image_url,
            "Description": self.description,
            "Author": self.author,
            "Servings": self.servings,
            "Ingredients": self.ingredients,
            "Cooking Steps": self.cooking_steps,
        }


@dataclass
class Category:
    title: str
    url: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(title=data.get("Title", ""), url=data.get("url", ""))

    def to_dict(self):
        return {"Title": self.title, "Url": self.url}
