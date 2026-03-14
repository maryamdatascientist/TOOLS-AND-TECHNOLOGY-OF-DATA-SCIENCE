import csv
import os
from collections import defaultdict

from scraper.crawler import CatalogCrawler


def deduplicate_by_url(records):
    seen = set()
    unique = []
    removed = 0

    for record in records:
        url = record.get("product_url")
        if url in seen:
            removed += 1
            continue
        seen.add(url)
        unique.append(record)

    return unique, removed


def export_products(products, filename="data/products.csv"):
    os.makedirs("data", exist_ok=True)

    fieldnames = [
        "category",
        "subcategory",
        "title",
        "price",
        "product_url",
        "image_url",
        "description",
        "reviews",
        "extra_spec",
        "source_page",
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)


def export_category_summary(products, duplicates_removed, filename="data/category_summary.csv"):
    os.makedirs("data", exist_ok=True)

    grouped = defaultdict(list)

    for product in products:
        grouped[product["subcategory"]].append(product)

    rows = []

    for subcategory, items in grouped.items():
        prices = [item["price"] for item in items if item["price"] is not None]

        average_price = round(sum(prices) / len(prices), 2) if prices else 0
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 0
        missing_descriptions = sum(1 for item in items if not item["description"])

        rows.append(
            {
                "subcategory": subcategory,
                "total_products": len(items),
                "average_price": average_price,
                "min_price": min_price,
                "max_price": max_price,
                "missing_descriptions": missing_descriptions,
                "duplicates_removed": duplicates_removed,
            }
        )

    fieldnames = [
        "subcategory",
        "total_products",
        "average_price",
        "min_price",
        "max_price",
        "missing_descriptions",
        "duplicates_removed",
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():

    base_url = "https://webscraper.io/test-sites/e-commerce/static"

    crawler = CatalogCrawler(base_url)

    categories = crawler.get_categories_and_subcategories()

    print("Categories discovered:", len(categories))

    all_products = []

    for item in categories:

        print("Processing:", item["subcategory"])

        product_links = crawler.get_product_links(item["url"])

        for link_data in product_links:
            
            product_url = link_data["url"]
            page_number = link_data["page"]

            try:

                details = crawler.get_product_details(product_url)

                details["category"] = item["category"]
                details["subcategory"] = item["subcategory"]
                details["source_page"] = page_number

                all_products.append(details)

            except Exception as e:
                print("Failed:", product_url, e)

    print("Products before dedup:", len(all_products))

    all_products, removed = deduplicate_by_url(all_products)

    print("Duplicates removed:", removed)
    print("Final products:", len(all_products))

    export_products(all_products)
    export_category_summary(all_products, removed)

    print("products.csv created")
    print("category_summary.csv created")


if __name__ == "__main__":
    main()
