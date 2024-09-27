from scraper import RecipeScraper

main_url = "https://kulinaria.ge"
my_category = "თევზი და ზღვის პროდუქტები"

# Create an instance of RecipeScraper
scraper = RecipeScraper(main_url, my_category)

# Scrape the recipes
scraper.scrape_recipes()

# Get the recipe list
recipe_list = scraper.get_recipes()