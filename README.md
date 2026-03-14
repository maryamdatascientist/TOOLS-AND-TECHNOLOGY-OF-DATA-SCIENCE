# TOOLS-AND-TECHNOLOGY-OF-DATA-SCIENCE
Catalog scrapper mini project

# Catalog Scraper Mini Project

## Project Purpose
This project is a mini web scraping project for the **Tools & Technology for Data Science** course. The target website is:

`https://webscraper.io/test-sites/e-commerce/static`

The scraper is built to start from the main catalog, discover categories and subcategories, follow paginated listing pages, collect product links, visit product detail pages, extract and clean the required data, and export the final datasets into CSV files.

It also demonstrates:
- Git/GitHub branching
- use of `uv` package manager
- scraping with `requests` and `beautifulsoup4`
- data cleaning and deduplication

---

## Project Structure
```text
project/
├── pyproject.toml
├── README.md
├── data/
│   ├── products.csv
│   └── category_summary.csv
├── src/
│   ├── main.py
│   └── scraper/
│       ├── crawler.py
│       ├── parsers.py
│       ├── exporters.py
│       └── utils.py
└── tests/
Setup with uv
This project was initialized and managed using uv.
Initialize the project:
uv init
Add dependencies:
uv add requests beautifulsoup4
If the project is already cloned, install everything using:
uv sync
Dependencies are managed in:
pyproject.toml
uv.lock
How to Run the Scraper
From the project root, run:
uv run python src/main.py
After running, the scraper generates:
data/products.csv
data/category_summary.csv
Scraper Workflow
The scraper performs these steps:
opens the main catalog page
discovers categories
discovers subcategories
follows paginated listing pages
collects product links from all pages
opens each product detail page
extracts and cleans product data
removes duplicate products
exports final CSV datasets
Extracted Data
For each product, the scraper extracts:
category
subcategory
product title
price
product URL
image URL
description
review count
important detail/spec field
source page number
Output Files
products.csv
Contains product-level data such as:
category
subcategory
title
price
description
reviews
image URL
product URL
source page
category_summary.csv
Contains summary statistics per subcategory, including:
total products
average price
minimum price
maximum price
count of missing descriptions
count of duplicates removed
Branch Workflow Followed
The required Git workflow was followed using these branches:
main
dev
feature/catalog-navigation
feature/product-details
fix/url-resolution
fix/deduplication
Workflow used:
created repository with main
created dev
created feature/catalog-navigation
implemented category, subcategory, and pagination navigation
created feature/product-details
implemented product detail scraping
merged both feature branches into dev
created fix/url-resolution
fixed relative URL handling
created fix/deduplication
fixed duplicate handling
merged fixes into dev
tested final project
merged dev into main
Assumptions Made
the website structure stays consistent
prices can be converted into numeric format after removing $
some products may have missing reviews or descriptions, so empty values are handled safely
the important detail/spec field can be taken from the product description if no separate field exists
pagination continues until no more products are found
duplicate products are identified using product URL
Limitations
this scraper is designed specifically for the target static website
if the HTML structure changes, selectors may need to be updated
review count is extracted only if available
extra specification data depends on what is available on the product page
the project uses simple synchronous requests, so it is not optimized for maximum speed
Selenium, Playwright, and Scrapy are not used, as required by the assignment