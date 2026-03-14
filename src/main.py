from scraper.crawler import CatalogCrawler
from scraper.exporters import export_products, export_category_summary
from scraper.utils import deduplicate_by_url


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