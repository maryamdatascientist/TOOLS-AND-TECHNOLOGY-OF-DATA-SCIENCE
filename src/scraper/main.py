import os
import sys
from pathlib import Path

try:
    from crawler import CatalogCrawler
except ModuleNotFoundError as exc:
    # If the user runs with system Python, dependencies like `requests` may be missing.
    if exc.name in {"requests", "bs4"}:
        # `.../src/scraper/main.py` -> repo root is 2 parents up from `src/`.
        repo_root = Path(__file__).resolve().parents[2]
        venv_python = repo_root / ".venv" / "bin" / "python"

        # Transparently re-run this script with the project venv if it exists.
        if venv_python.exists() and venv_python.is_file() and sys.executable != str(venv_python):
            os.execv(str(venv_python), [str(venv_python), *sys.argv])

        raise ModuleNotFoundError(
            f"Missing dependency '{exc.name}'. Run with the project venv: "
            f"`.venv/bin/python src/scraper/main.py`"
        ) from None
    raise


def main() -> None:
    base_url = "https://webscraper.io/test-sites/e-commerce/static"
    crawler = CatalogCrawler(base_url)

    categories = crawler.get_categories_and_subcategories()

    print("Discovered category/subcategory links:\n")

    for item in categories:
        category = item["category"]
        subcategory = item["subcategory"] if item["subcategory"] else "No subcategory"
        url = item["url"]
        print(f"{category} | {subcategory} -> {url}")


if __name__ == "__main__":
    main()
    
