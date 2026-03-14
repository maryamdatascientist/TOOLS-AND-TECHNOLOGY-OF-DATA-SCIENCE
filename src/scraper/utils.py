from urllib.parse import urljoin
import re
import requests


def safe_join(base: str, href: str) -> str:
    return urljoin(base, href)


def clean_text(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def parse_price(price_str: str):
    """
    "$416.99" -> 416.99 (float) or None if missing
    """
    if not price_str:
        return None
    price_str = price_str.replace("$", "").strip()
    try:
        return float(price_str)
    except Exception:
        return None


def safe_get(session: requests.Session, url: str, timeout: int = 30) -> str:
    resp = session.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def deduplicate_by_url(records):
    seen = set()
    unique = []
    removed = 0

    for r in records:
        url = r.get("product_url")
        if url in seen:
            removed += 1
            continue
        seen.add(url)
        unique.append(r)

    return unique, removed