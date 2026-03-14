import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class CatalogCrawler:

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})

    def fetch_page(self, url):
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    def get_soup(self, html):
        return BeautifulSoup(html, "html.parser")

    # ---------------------------------
    # CATEGORY + SUBCATEGORY DISCOVERY
    # ---------------------------------
    def get_categories_and_subcategories(self):

        categories = [
            {
                "category": "Computers",
                "subcategory": "Laptops",
                "url": f"{self.base_url}/computers/laptops"
            },
            {
                "category": "Computers",
                "subcategory": "Tablets",
                "url": f"{self.base_url}/computers/tablets"
            },
            {
                "category": "Phones",
                "subcategory": "Touch",
                "url": f"{self.base_url}/phones/touch"
            }
        ]

        return categories

    # ---------------------------------
    # PAGINATION
    # ---------------------------------
    def get_pagination_links(self, url):
        pages = []
        page_number = 1

        while True:
            if page_number == 1:
                page_url = url
            else:
                page_url = f"{url}?page={page_number}"

            html = self.fetch_page(page_url)
            soup = self.get_soup(html)

            products = soup.select("a.title")
            if not products:
                break

            pages.append(page_url)
            page_number += 1

        return pages

    # ---------------------------------
    # PRODUCT LINKS
    # ---------------------------------
    def get_product_links(self, url):
        pages = self.get_pagination_links(url)

        links = []
        seen = set()

        for page_number, page in enumerate(pages, start=1):
            html = self.fetch_page(page)
            soup = self.get_soup(html)

            products = soup.select("a.title")

            for p in products:
                href = p.get("href")
                if not href:
                    continue

                product_url = urljoin(self.base_url, href)

                if product_url not in seen:
                    seen.add(product_url)
                    links.append({
                        "url": product_url,
                        "page": page_number
                    })

        return links

    # ---------------------------------
    # PRODUCT DETAILS
    # ---------------------------------
    def get_product_details(self, url):

        html = self.fetch_page(url)
        soup = self.get_soup(html)

        title_tag = soup.select_one("h4.title")
        price_tag = soup.select_one("h4.price")
        desc_tag = soup.select_one(".description")
        review_tag = soup.select_one(".ratings .pull-right")
        image_tag = soup.select_one(".img-responsive")

        title = title_tag.text.strip() if title_tag else ""

        price = None
        if price_tag:
            price = float(price_tag.text.replace("$", "").strip())

        description = desc_tag.text.strip() if desc_tag else ""

        reviews = ""
        if review_tag:
            reviews = review_tag.text.split()[0]

        image_url = ""
        if image_tag and image_tag.get("src"):
            image_url = urljoin(self.base_url, image_tag.get("src"))

        return {
            "title": title,
            "price": price,
            "description": description,
            "reviews": reviews,
            "image_url": image_url,
            "extra_spec": description,
            "product_url": url
        }