# Recipe Scraper
## Overview

This Python project is designed to scrape recipes from a website, store them in a `MongoDB` database and extract useful statistics from the stored data. It uses the `BeautifulSoup` library to parse HTML and extract recipe details such as title, author, description, ingredients, and cooking steps. The script supports scraping specific categories of recipes and their subcategories. The goal is to efficiently scrape, store, and analyze recipes from the assigned category.

## Features
- Scrape recipes from a specified category and its subcategories.
- Extract relevant recipe details including:
  - Title
  - URL of the recipe
  - Main category and subcategory
  - Author
  - Description
  - Ingredients
  - Cooking steps
  - Portion size
  - Image URL

## Data Storage

Once the data is scraped, it is processed and stored in a **MongoDB** database. Each recipe is saved as a document with fields corresponding to the details above (title, category, ingredients, etc.).

## Statistics Extraction

After storing the recipe data, the following useful statistics can be extracted from the database:

1. **Average Number of Ingredients**: Calculates the average number of ingredients across all stored recipes.
2. **Average Number of Preparation Steps**: Finds the average number of preparation steps per recipe.
3. **Recipe with the Most Servings**: Identifies and returns the recipe with the highest number of servings.
4. **Author with the Most Recipes**: Determines which author has the most recipes published, returning their name and number of recipes.

## Project Structure

- **`scraper.py`**: Handles web scraping, fetching recipe details from the assigned category.
- **`recipe.py`**: Defines the `Recipe` class to model the structure of the scraped recipe data.
- **`recipe_repository.py`**: Contains the `RecipeRepository` class, responsible for storing and retrieving data and data statistics from MongoDB.

## Dependencies

- **Python 3.11**
- **BeautifulSoup4**: for HTML parsing and scraping web data.
- **Requests**: to fetch the HTML content of web page.
- **MongoDB**: for storing the scraped data.
- **PyMongo**: for database interactions.
