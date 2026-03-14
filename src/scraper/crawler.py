import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class CatalogCrawler:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0"
            }
        )

    def fetch_page(self, url: str) -> str:
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    def get_soup(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "html.parser")

    def get_categories_and_subcategories(self) -> list[dict]:
        results = []
        seen = set()

        main_html = self.fetch_page(self.base_url)
        main_soup = self.get_soup(main_html)

        category_links = main_soup.select("a.category-link")

        for category_link in category_links:
            category_name = category_link.get_text(strip=True)
            category_href = category_link.get("href")

            if not category_href:
                continue

            category_url = urljoin(self.base_url, category_href)

            if category_url not in seen:
                seen.add(category_url)
                results.append(
                    {
                        "category": category_name,
                        "subcategory": None,
                        "url": category_url,
                    }
                )

            category_html = self.fetch_page(category_url)
            category_soup = self.get_soup(category_html)

            subcategory_links = category_soup.select("a.subcategory-link")

            for sub_link in subcategory_links:
                sub_name = sub_link.get_text(strip=True)
                sub_href = sub_link.get("href")

                if not sub_href:
                    continue

                sub_url = urljoin(self.base_url, sub_href)

                if sub_url not in seen:
                    seen.add(sub_url)
                    results.append(
                        {
                            "category": category_name,
                            "subcategory": sub_name,
                            "url": sub_url,
                        }
                    )

        return results
