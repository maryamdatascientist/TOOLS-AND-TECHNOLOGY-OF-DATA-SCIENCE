from bs4 import BeautifulSoup
from .utils import clean_text, parse_price


def get_soup(html: str):
    return BeautifulSoup(html, "html.parser")


def parse_categories_and_subcategories(soup, base_url, join):
    results = []
    seen = set()

    categories = soup.select("a.category-link")

    for cat in categories:
        category = clean_text(cat.text)
        href = cat.get("href")
        if not href:
            continue

        cat_url = join(base_url, href)

        if cat_url not in seen:
            seen.add(cat_url)
            results.append({
                "category": category,
                "subcategory": None,
                "url": cat_url
            })

    return results


def parse_subcategories(soup, category, base_url, join, seen):
    results = []

    subs = soup.select(".subcategory a")

    for s in subs:
        href = s.get("href")
        if not href:
            continue

        sub_url = join(base_url, href)

        if sub_url not in seen:
            seen.add(sub_url)
            results.append({
                "category": category,
                "subcategory": clean_text(s.text),
                "url": sub_url
            })

    return results


def parse_pagination(soup, base_url, join):
    pages = []
    links = soup.select("ul.pagination li a")

    for a in links:
        href = a.get("href")
        if not href:
            continue
        pages.append(join(base_url, href))

    return pages


def parse_product_links(soup, base_url, join):
    links = []

    products = soup.select("a.title")

    for p in products:
        href = p.get("href")
        if not href:
            continue

        links.append(join(base_url, href))

    return links


def parse_product_details(soup, base_url, join):

    title_tag = soup.select_one("h4.title")
    price_tag = soup.select_one("h4.price")
    desc_tag = soup.select_one(".description")
    review_tag = soup.select_one(".ratings .pull-right")
    image_tag = soup.select_one(".img-responsive")

    title = clean_text(title_tag.text) if title_tag else ""
    price = parse_price(price_tag.text) if price_tag else None
    description = clean_text(desc_tag.text) if desc_tag else ""

    reviews = ""
    if review_tag:
        reviews = clean_text(review_tag.text).split()[0]

    image_url = ""
    if image_tag and image_tag.get("src"):
        image_url = join(base_url, image_tag.get("src"))

    return {
        "title": title,
        "price": price,
        "description": description,
        "reviews": reviews,
        "image_url": image_url,
        "extra_spec": description
    }