from bs4 import BeautifulSoup
import requests
import re

# Create class for scrapping
class RecipeScraper:
    # Initialize the RecipeScraper with the main URL and the category to scrape.
    def __init__(self, main_url, category):
        self.main_url = main_url
        self.category = category
        self.recipe_list = []

    # Fetch the HTML content of the provided URL and return a BeautifulSoup object.
    def get_soup(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")

    # Scrape the main recipe category page and find the URL for the desired category.
    def scrape_category(self):
        main_soup = self.get_soup(self.main_url)
        recipes_url = self.main_url + main_soup.find('a', class_="nav__item recipe-nav-text").attrs['href']
        recipes_soup = self.get_soup(recipes_url)
        category_url = self.main_url + recipes_soup.find("div", string=self.category).find_parent("a").attrs['href']
        return self.get_soup(category_url), category_url

    # Scrape and return all subcategories from the category page.
    def scrape_subcategories(self, category_soup):
        subcategories = category_soup.find("div", class_="recipe__nav--view").find_all("a", class_="recipe__nav-item")
        return subcategories

    def extract_recipe_data(self, recipe_soup):

        # Extract portion size (if available)
        portion_text = recipe_soup.find('div', class_="kulinaria-sprite kulinaria-sprite--circleprogress").find_parent(
            'div').text.strip()
        match = re.search(r'\d+', portion_text)
        portion = int(match.group()) if match else 0

        # Extract ingredients
        recipe_ingredients = recipe_soup.find_all("div", class_="list__item")
        ingredients = []
        for ingredient in recipe_ingredients:
            raw_text = ingredient.get_text(separator=' ', strip=True)
            clean_text = ' '.join(raw_text.split())
            ingredients.append(clean_text)

        # Extract cooking steps
        steps = [f"{step.div.text}. {step.p.text.strip()}" for step in
                 recipe_soup.find_all("div", class_="lineList__item")]
        return portion, ingredients, steps

    # Scrape all recipes from the selected category and subcategories, and store them in recipe_list.
    def scrape_recipes(self):
        # Scrape the category page and get the subcategories
        category_soup, category_url = self.scrape_category()
        subcategories = self.scrape_subcategories(category_soup)

        # Loop each subcategory
        for subcategory in subcategories:
            subcategory_title = subcategory.find("div", class_="txt").text
            subcategory_url = self.main_url + subcategory.attrs['href']
            subcategory_soup = self.get_soup(subcategory_url)

            # Find all recipes within the subcategory
            recipes = subcategory_soup.find_all("div", class_="box box--author kulinaria-col-3 box--massonry")
            for recipe in recipes:
                title = recipe.find('a', class_="box__title").text.strip()
                author = recipe.find('div', class_="name").text.strip()
                desc = recipe.find('div', class_="box__desc").text.strip()
                image_url = self.main_url + recipe.find('img').attrs['src']
                recipe_url = self.main_url + recipe.find('a', class_="box__title").attrs['href']

                recipe_soup = self.get_soup(recipe_url)
                portion, ingredients, steps = self.extract_recipe_data(recipe_soup)

                # Append the scraped recipe to the recipe list
                self.recipe_list.append(
                    {
                        "Title": title,
                        "Recipe URL": recipe_url,
                        "Main Category": {"Title": self.category, "url": category_url},
                        "Subcategory": {"Title": subcategory_title, "url": subcategory_url},
                        "Image URL": image_url,
                        "Description": desc,
                        "Author": author,
                        "Portion": portion,
                        "Ingredients": ingredients,
                        "Cooking Steps": steps
                    }
                )

    # Return the list of all scraped recipes.
    def get_recipes(self):
        return self.recipe_list