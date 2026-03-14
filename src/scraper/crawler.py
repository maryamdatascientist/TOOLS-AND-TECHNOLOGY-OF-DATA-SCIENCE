import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class CatalogCrawler:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})

    def fetch_page(self, url: str) -> str:
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    def get_soup(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "html.parser")

    def get_categories_and_subcategories(self):
        # Explicit subcategory targets for this assignment site
        return [
            {
                "category": "Computers",
                "subcategory": "Laptops",
                "url": f"{self.base_url}/computers/laptops",
            },
            {
                "category": "Computers",
                "subcategory": "Tablets",
                "url": f"{self.base_url}/computers/tablets",
            },
            {
                "category": "Phones",
                "subcategory": "Touch",
                "url": f"{self.base_url}/phones/touch",
            },
        ]

    def get_product_links(self, category_url: str):
        """
        Crawl pages as:
        page 1 -> category_url
        page 2 -> category_url?page=2
        ...
        Stop when a page has no products.
        """
        links = []
        seen = set()
        page = 1

        while True:
            if page == 1:
                page_url = category_url
            else:
                page_url = f"{category_url}?page={page}"

            html = self.fetch_page(page_url)
            soup = self.get_soup(html)

            products = soup.select("a.title")

            if not products:
                break

            for product in products:
                href = product.get("href")
                if not href:
                    continue

                product_url = urljoin(self.base_url + "/", href)

                if product_url not in seen:
                    seen.add(product_url)
                    links.append(
                        {
                            "url": product_url,
                            "page": page,
                        }
                    )

            page += 1

        return links

    def get_product_details(self, product_url: str):
        html = self.fetch_page(product_url)
        soup = self.get_soup(html)

        title_tag = soup.select_one("h4.title")
        price_tag = soup.select_one("h4.price")
        desc_tag = soup.select_one(".description")
        review_tag = soup.select_one(".ratings .pull-right")
        image_tag = soup.select_one(".img-responsive")

        title = title_tag.get_text(strip=True) if title_tag else ""

        price = None
        if price_tag:
            raw_price = price_tag.get_text(strip=True).replace("$", "")
            try:
                price = float(raw_price)
            except ValueError:
                price = None

        description = desc_tag.get_text(" ", strip=True) if desc_tag else ""

        reviews = ""
        if review_tag:
            reviews = review_tag.get_text(strip=True).split()[0]

        image_url = ""
        if image_tag and image_tag.get("src"):
            image_url = urljoin(self.base_url + "/", image_tag.get("src"))

        extra_spec = description

        return {
            "title": title,
            "price": price,
            "description": description,
            "reviews": reviews,
            "image_url": image_url,
            "extra_spec": extra_spec,
            "product_url": product_url,
        }